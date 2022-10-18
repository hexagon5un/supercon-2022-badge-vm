# assemble.py
# Adam Zeloof
# 9.17.2022
## Revised by Elliot Williams 10.18.2022 


DEBUG=False

class Assembler:
    
    def strip_and_split(self, instruction):
        ins = instruction.split(" ", 1) ## split op/arg on first whitespace
        op = ins[0].lower()  ## regularize to lowercase, strip spaces
        args = ins[1].split(",")
        args = [x.strip().lower() for x in args]
        if DEBUG:
            print(op, args)
        return((op, args))

    def lookup(self, instruction):
        op, args = strip_and_split(instruction)

    def handle_R0_ops(self, opcode, args):
        if args[1].startswith("r"):
            # RX,RY
            x = number(args[0])
            y = number(args[1])
            return (opcode, x, y)
        else:
            # R0,N
            n = number(args[1])
            return (0x0, opcode, n)
 
    def handle_generic_short_op(self, opcode, args):
        assert( len(args)==2 )
        args = [number(x) for x in args] 
        return (opcode, args[0], args[1])
    
    def handle_generic_long_op(self, opcode, args):
        # R0, N or Ry 
        if len(args) == 1:
            return (0, opcode, number(args[0]))
        else:
            return (0, opcode, number(args[1]))
    
    def handle_bitwise_ops(self, opcode, args):
        # RG, M
        g = number(args[0])
        m = number(args[1])
        assert(g < 4)
        assert(m < 4)
        gm = (g << 2) + m 
        return (0, opcode, gm)
    
    def handle_skip(self, opcode, args):
        # F, M
        f = ["z","nz","c","nc"].index(args[0])
        m = number(args[1])
        if m == 0: 
            m = 4
        fm = (f << 2) + m
        return(0, opcode, fm)

    def handle_jr(self, opcode, args):
        ## NN is a signed 8 bit
        nn = number(args[0])
        if not args[0].startswith("0b") and not args[0].startswith("0x"):
            nn = twos_comp(nn, 8)
        n0, n1 = byte_to_nibbles(nn)
        return (0xf, n0, n1)
    
    def handle_mov(self, opcode, args):
        # print(opcode,args)
        if args[0].startswith('r') and args[1].startswith('r'):
            # RX,RY
            return (0x8, number(args[0]), number(args[1]))
        elif ':' in args[0]:
            # [X:Y],R0
            xy = args[0].strip('[]').split(":")
            return (0xa, number(xy[0]), number(xy[1]))
        elif ':' in args[1]:
            # R0,[X:Y]
            xy = args[1].strip('[]').split(":")
            return (0xb, number(xy[0]), number(xy[1]))
        elif args[0].startswith('['):
            # [NN],R0
            nn = number(args[0].strip('[]'))
            n0, n1 = byte_to_nibbles(nn)
            return (0xc, n0 , n1)
        elif args[1].startswith('['):
            # R0,[NN]
            nn = number(args[1].strip('[]'))
            n0, n1 = byte_to_nibbles(nn)
            return (0xd, n0, n1)
        elif args[0].startswith('r'):
            # RX,N
            return (0x9, number(args[0]), number(args[1]))
        elif args[0] == 'pc':
            # PC,NN
            nn = number(args[1])
            n0, n1 = byte_to_nibbles(nn)
            return (0xe, n0, n1)
 
    # a lookup dictionary of instructions, the functions that handle them, and their opcodes
    # and, or, add, and xor have Rx,Ry versions, and R0, n versions 
    # MOV is its own monster
    handlers = {"add":(handle_R0_ops, 1), 
                "adc":(handle_generic_short_op, 2),
                "sub":(handle_generic_short_op, 3),
                "sbb":(handle_generic_short_op, 4),
                "or" :(handle_R0_ops, 5),
                "and":(handle_R0_ops, 6),
                "xor":(handle_R0_ops, 7),
                "mov":(handle_mov, None), ## many different opcodes here!
                "jr": (handle_jr, 15), ## needs own b/c 16-bit argument 
                "cp": (handle_generic_long_op, 0),
                "inc":(handle_generic_long_op, 2),
                "dec":(handle_generic_long_op, 3),
                "dsz":(handle_generic_long_op, 4),
                "exr":(handle_generic_long_op, 8),
                "bit":(handle_bitwise_ops, 9), ## RG, M packed into 4 bits
                "bset":(handle_bitwise_ops, 10),
                "bclr":(handle_bitwise_ops, 11),
                "btg":(handle_bitwise_ops, 12),
                "rrc":(handle_generic_long_op, 13),
                "ret":(handle_generic_long_op, 14),
                "skip":(handle_skip, 15) ## flag encoding 
                }

    def assemble_single_command(self, command):
        op, args = self.strip_and_split(command)
        handler, opcode = self.handlers[op]
        x, y, z = handler(self, opcode, args)
        return (x,y,z)
    
    def read(self, filename=None):
        if not filename: 
            filename = self.infile
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split('//')[0]
                if line:
                    self.assembly_language.append(line)

    def assemble(self, instructions=None):
        if not instructions:
            instructions=self.assembly_language
        for line in instructions:
            assembled = self.assemble_single_command(line)
            self.machine_language.append(assembled)
    
    def write(self, filename=None):
        if not filename: 
            filename = self.outfile
        with open(filename, 'wb') as f:
            header = (0x00, 0xff, 0x00, 0xff, 0xa5, 0xc3)
            length = len(self.machine_language)
            for b in header:
                f.write(b.to_bytes(1, byteorder='little', signed=False))
            f.write(length.to_bytes(2, byteorder='little', signed=False))
            for ins in self.machine_language:
                assert(len(ins) == 3)
                A = (ins[1] << 4) + ins[2]
                B = ins[0]
                f.write(A.to_bytes(1, byteorder='little', signed=False))
                f.write(B.to_bytes(1, byteorder='little', signed=False))
            # TODO write checksum


    def __init__(self, infile=None):
        self.machine_language = []
        self.assembly_language = []
        self.infile = infile

        ## pass it a filename and it assembles it
        if infile:
            self.outfile = infile.split(".")[0]+".bin"
            self.read()
            self.assemble()
            self.write()

## Utility functions here 
def number(n):
    n = n.lower()
    if n.startswith("0x"):
        return int(n[2:], 16)
    elif n.startswith("0b"):
        return int(n[2:], 2)
    elif n.startswith("r"): # register number
        if n == "rs":  ## handles strange case with bit ops
            return(3)
        else:
            return int(n[1:])
    else:
        return int(n)

def twos_comp(n, bits):
    assert(n in range(-2**(bits-1), 2**(bits-1)))  ## in range? 
    return n & (2**bits-1)

def byte_to_nibbles(byte):
    n0 = byte >> 4
    n1 = byte & 0b00001111
    return (n0, n1)

def pad(n, b):
    if len(n) < b:
        n = '0'*(b-len(n)) + n
    elif len(n) > b:
        pass
    return n

def bits(n, b):
    # takes an int n and int b
    # returns a string of n represented in binary with b bits
    return pad(bin(n).split('b')[1],b)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        a = Assembler(sys.argv[1])
        print(f"Wrote {a.outfile}")
    else:
        print ("""Usage: python assemble.py filename.bvm""")

