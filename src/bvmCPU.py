# bvmCPU.py
# Adam Zeloof
# 3.12.2022
# requires Python 3.10 or higher


def pad(n, b):
    if len(n) < b:
        n = '0'*(b-len(n)) + n
    elif len(n) > b:
        pass
    return n

def signed(n, b):
    # https://stackoverflow.com/questions/1604464/twos-complement-in-python
    if (n & (1 << (b - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        n = n - (1 << b)        # compute negative value
    return n     


def bits(n, b):
    # takes an int n and int b
    # returns a string of n represented in binary with b bits
    return pad(bin(n).split('b')[1],b)


class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.sp = 0
        self.pc = 0

        # Flags
        self.V = 0
        self.Z = 0
        self.C = 0


    def getPC(self):
        #pcl = self.ram[13]
        #pcm = self.ram[14] << 4
        #pch = self.ram[15] << 8
        #return pch | pcm | pcl
        return self.pc


    def setPC(self, pc):
        #pc = bin(pc % 4096).split('b')[1]
        #pc = pad(pc, 12)
        #self.ram[13] = int(pc[8:12],2)
        #self.ram[14] = int(pc[4:8],2)
        #self.ram[15] = int(pc[0:4],2)
        self.pc = pc % 4096


    def step(self):
        pc = self.getPC() + 1
        self.setPC(pc)


    def handleJumps(self, dest):
        if dest == 0x0c:
            # dest is JSR, execute a subroutine call
            pc = bin(self.pc % 4096).split('b')[1]
            pc = pad(pc, 12)
            self.sp = (self.sp + 1) % 8
            # Load the current PC into the stack
            self.ram[0x10+self.sp*3-3] = int(pc[8:12],2)#self.ram[0x0d]
            self.ram[0x10+self.sp*3-2] = int(pc[4:8],2)#self.ram[0x0e]
            self.ram[0x10+self.sp*3-1] = int(pc[0:4],2)#self.ram[0x0f]
            # Set the PC
            jsr = self.ram[0x0c]
            pcm = self.ram[0x0e] << 4
            pch = self.ram[0x0f] << 8
            self.pc = pch | pcm | jsr - 1 # Unsure if -1 is needed, compare to real badge
        elif dest == 0x0d:
            # dest is PCL, execute a program jump
            pcl = self.ram[0x0d]
            pcm = self.ram[0x0e] << 4
            pch = self.ram[0x0f] << 8
            self.pc = pch | pcm | pcl - 1 # Unsure if -1 is needed, compare to real badge
            pass


    def ADD(self, args):
        if args['mode'] == 0:
            # RX,RY
            x = args['x']
            y = args['y']
            a = self.ram[x]
            b = self.ram[y]
            res = a + b
            self.ram[x] = res % 16
            if res > 15:
                self.C = 1
            else:
                self.C = 0
            if res == 0:
                self.Z = 1
            else:
                self.Z = 0
            if (signed(a, 4) + signed(b, 4) > 7) or (signed(a, 4) + signed(b, 4) < -8):
                self.V = 1
            else:
                self.V = 0

        elif args['mode'] == 1: # R0,N
            a = self.ram[0]
            b = args['n']
            res = a + b
            self.ram[0] = res % 16
            if res > 15:
                self.C = 1
            else:
                self.C = 0
            if res == 0:
                self.Z = 1
            else:
                self.Z = 0
            if (signed(a, 4) + signed(b, 4) > 7) or (signed(a, 4) + signed(b, 4) < -8):
                self.V = 1
            else:
                self.V = 0
    

    def ADC(self, args):
        x = args['x']
        y = args['y']
        a = self.ram[x]
        b = self.ram[y]
        res = a + b + self.C
        self.ram[x] = res % 16
        # I think the docs are wrong here, using same behaivor as ADD regarding overflow
        if res > 15:
            self.C = 1
        else:
            self.C = 0
        if res == 0:
            self.Z = 1
        else:
            self.Z = 0
        if (signed(a, 4) + signed(b, 4) + self.C > 7) or (signed(a, 4) + signed(b, 4) + self.C < -8):
            self.V = 1
        else:
            self.V = 0
    

    def SUB(self, args):
        x = args['x']
        y = args['y']
        a = self.ram[x]
        b = self.ram[y]
        res = a - b
        self.ram[x] = res % 16
        if res < 0:
            self.C = 1
        else:
            self.C = 0
        if res == 0:
            self.Z = 1
        else:
            self.Z = 0
        if (signed(a, 4) - signed(b, 4) > 7) or (signed(a, 4) - signed(b, 4) < -8):
            self.V = 1
        else:
            self.V = 0
    

    def SBB(self, args):
        x = args['x']
        y = args['y']
        a = self.ram[x]
        b = self.ram[y]
        res = a - b - int(self.C==0)
        self.ram[x] = res % 16
        if res < 0:
            self.C = 1
        else:
            self.C = 0
        if res == 0:
            self.Z = 1
        else:
            self.Z = 0
        if (signed(a, 4) - signed(b, 4)  - int(self.C==0) > 7) or (signed(a, 4) - signed(b, 4) - int(self.C==0) < -8):
            self.V = 1
        else:
            self.V = 0
    

    def OR(self, args):
        if args['mode'] == 0:
            x = args['x']
            y = args['y']
            self.ram[x] = self.ram[x] | self.ram[y]
            if self.ram[x] == 0:
                self.Z = 1
            else:
                self.Z = 0
        elif args['mode'] == 1:
            n = args['n']
            self.ram[0] = self.ram[0] | n
            if self.ram[0] == 0:
                self.Z = 1
            else:
                self.Z = 0
    

    def AND(self, args):
        if args['mode'] == 0:
            x = args['x']
            y = args['y']
            self.ram[x] = self.ram[x] & self.ram[y]
            if self.ram[x] == 0:
                self.Z = 1
            else:
                self.Z = 0
        elif args['mode'] == 1:
            n = args['n']
            self.ram[0] = self.ram[0] & n
            if self.ram[0] == 0:
                self.Z = 1
            else:
                self.Z = 0
    

    def XOR(self, args):
        if args['mode'] == 0:
            x = args['x']
            y = args['y']
            self.ram[x] = self.ram[x] ^ self.ram[y]
            if self.ram[x] == 0:
                self.Z = 1
            else:
                self.Z = 0
        elif args['mode'] == 1:
            n = args['n']
            self.ram[0] = self.ram[0] ^ n
            if self.ram[0] == 0:
                self.Z = 1
            else:
                self.Z = 0
    

    def MOV(self, args):
        if args['mode'] ==  0: # RX,RY
            x = args['x']
            y = args['y']
            self.ram[x] = self.ram[y]
            self.handleJumps(x)
        elif args['mode'] ==  1: # RX,N
            x = args['x']
            n = args['n']
            self.ram[x] = n
            self.handleJumps(x)
        elif args['mode'] ==  2: # XY,R0
            rx = self.ram[args['x']]
            ry = self.ram[args['y']]
            addr = rx << 4 | ry
            self.ram[addr] = self.ram[0]
        elif args['mode'] ==  3: # R0,XY
            rx = self.ram[args['x']]
            ry = self.ram[args['y']]
            addr = rx << 4 | ry
            self.ram[0] = self.ram[addr]
        elif args['mode'] ==  4: # NN,R0
            self.ram[args['nn']] = self.ram[0]
        elif args['mode'] ==  5: # R0,NN
            self.ram[0] = self.ram[args['nn']]
        elif args['mode'] ==  6: # PC,NN
            nnBin = bin(args['nn']).split('b')[1]
            if len(nnBin) < 8:
                nnBin = '0'*(8-len(nnBin)) + nnBin
            self.ram[14] = nnBin[4:8]
            self.ram[15] = nnBin[0:4]
    

    def JR(self, args):
        pc = self.getPC()
        pc += signed(args['nn'], 8)
        self.setPC(pc)
    

    def CP(self, args):
        r0 = self.ram[0]
        n = args['n']
        if (r0 > n) or (r0 == n):
            self.C = 1
        else:
            self.C = 0
        if r0 == n:
            self.Z = 1
        else:
            self.Z = 0
    

    def INC(self, args):
        y = args['y']
        self.ram[y] = (self.ram[y] + 1) % 16
        self.handleJumps(y)
        if self.ram[y] == 0:
            self.Z = 1
        else:
            self.Z = 0


    def DEC(self, args):
        y = args['y']
        self.ram[y] = (self.ram[y] - 1) % 16
        self.handleJumps(y)
        if self.ram[y] == 0:
            self.Z = 1
        else:
            self.Z = 0
    

    def DSZ(self, args):
        y = args['y']
        self.ram[y] = (self.ram[y] - 1) % 16
        if self.ram[y] == 0:
            self.step()
    

    def EXR(self, args):
        n = args['n']
        for i in range(0, (n-1)%16+1):
            r = self.ram[i]
            p = self.ram[0xE + r]
            self.ram[i] = p
            self.ram[0xE + r] = r
    

    def BIT(self, args):
        r = self.ram[args['g']]
        bit = int(bin(r).split('b')[1][3-args['m']])
        if bit:
            self.Z = 0
        else:
            self.Z = 1
    

    def BSET(self, args):
        r = self.ram[args['g']]
        rBin = list(bits(r,4))
        rBin[3-args['m']] = "1"
        self.ram[args['g']] = int("".join(rBin),2)
        assert self.ram[args['g']] < 16
    

    def BCLR(self, args):
        r = self.ram[args['g']]
        rBin = list(bits(r,4))
        rBin[3-args['m']] = "0"
        self.ram[args['g']] = int("".join(rBin),2)
        assert self.ram[args['g']] < 16
    

    def BTG(self, args):
        r = self.ram[args['g']]
        bit = int(bits(r,4)[3-args['m']])
        rBin = list(bits(r,4))
        rBin[3-args['m']] = str((bit+1)%2)
        self.ram[args['g']] = int("".join(rBin),2)
        assert self.ram[args['g']] < 16
    

    def RRC(self, args):
        y = args['y']
        r = self.ram[y]
        rBin = bin(r).split('b')[1]
        lsb = rBin[3]
        rBin = str(self.C) + rBin[0:2]
        self.ram[y] = int(rBin,2)
        self.C = int(lsb)
        assert self.ram[y] < 16


    def RET(self, args):
        self.ram[0] = args['n']
        #self.ram[13] = self.ram[0x10+self.sp*3-3]
        #self.ram[14] = self.ram[0x10+self.sp*3-2]
        #self.ram[15] = self.ram[0x10+self.sp*3-1]
        pcl = self.ram[0x10+self.sp*3-3]
        pcm = self.ram[0x10+self.sp*3-2] << 4
        pch = self.ram[0x10+self.sp*3-1] << 8
        self.pc = pch | pcm | pcl
        self.sp = (self.sp - 1) % 8
    

    def SKIP(self, args):
        f = args['f']
        m = args['m']
        skip = False
        if f ==  0b00: # C
            if self.C:
                skip = True
        elif f ==  0b01: # NC
            if not self.C:
                skip = True
        elif f ==  0b10: # Z
            if self.Z:
                skip = True
        elif f ==  0b11: # NZ
            if not self.Z:
                skip = True
        if skip:
            pc = self.getPC()
            pc += (m-1)%4+1
            self.setPC(pc)
    
