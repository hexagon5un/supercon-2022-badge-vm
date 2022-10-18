# bvmParser.py
# Adam Zeloof
# 3.12.2022
# requires Python 3.10 or higher

def format(n):
    if len(n) < 2:
        return int(n)
    else:
        if n[0:2] == '0x':
            return int(n[2:],16)
        elif n[0:2] == '0b':
            return int(n[2:],2)
        else:
            return int(n)

def parse(instruction, mode):
    if mode == "bin":
        # Convert to a binary string, drop the leading '0b'
        instruction = instruction.replace(" ","")
        bIns = bin(int(instruction,2)).split('b')[1]

        # If < 12 bits, left pad with zeros
        if len(bIns) < 12:
            bIns = '0'*(12-len(bIns)) + bIns
        
        # Split up the instruction
        op4 = int(bIns[0:4],2)
        op8 = int(bIns[0:8],2)
        x   = int(bIns[4:8],2)
        y   = int(bIns[8:12],2)
        g   = int(bIns[8:10],2)
        f   = int(bIns[8:10],2)
        m   = int(bIns[10:12],2)
        n   = int(bIns[8:12],2)
        nn  = int(bIns[4:12],2)

        if op4 != 0:
            # We have a four-bit opcode
            if op4 ==  1: # ADD RX,RY
                return {
                    'op': 'ADD',
                    'args': {'mode':0, 'x':x, 'y':y}
                    }
            elif op4 ==  2: # ADC RX,RY
                return {
                    'op': 'ADC',
                    'args': {'x':x, 'y':y}
                    }
            elif op4 ==  3: # SUB RX,RY
                return {
                    'op': 'SUB',
                    'args': {'x':x, 'y':y}
                    }
            elif op4 ==  4: # SBB RX,RY
                return {
                    'op': 'SBB',
                    'args': {'x':x, 'y':y}
                    }
            elif op4 ==  5: # OR RX,RY
                return {
                    'op': 'OR',
                    'args': {'mode':0, 'x':x, 'y':y}
                    }
            elif op4 ==  6: # AND RX,RY
                return {
                    'op': 'AND',
                    'args': {'mode':0, 'x':x, 'y':y}
                    }
            elif op4 ==  7: # XOR RX,RY
                return {
                    'op': 'XOR',
                    'args': {'mode':0, 'x':x, 'y':y}
                    }
            elif op4 ==  8: # MOV RX,RY
                return {
                    'op': 'MOV',
                    'args': {'mode':0, 'x':x, 'y':y}
                    }
            elif op4 ==  9: # MOV RX,N
                return {
                    'op': 'MOV',
                    'args': {'mode':1, 'x':x, 'n':n}
                    }
            elif op4 ==  10: # MOV [XY],R0
                return {
                    'op': 'MOV',
                    'args': {'mode':2, 'x':x, 'y':y}
                    }
            elif op4 ==  11: # MOV R0,[XY]
                return {
                    'op': 'MOV',
                    'args': {'mode':3, 'x':x, 'y':y}
                    }
            elif op4 ==  12: # MOV [NN],R0
                return {
                    'op': 'MOV',
                    'args': {'mode':4, 'nn':nn}
                    }
            elif op4 ==  13: # MOV R0,[NN]
                return {
                    'op': 'MOV',
                    'args': {'mode':5, 'nn':nn}
                    }
            elif op4 ==  14: # MOV PC,NN
                return {
                    'op': 'MOV',
                    'args': {'mode':6, 'nn':nn}
                    }
            elif op4 ==  15: # JR NN
                return {
                    'op': 'JR',
                    'args': {'nn':nn}
                    }
        else:
            # We have an eight-bit opcode
            if op8 ==  0: # CP R0,N
                return {
                    'op': 'CP',
                    'args': {'n':n}
                }
            elif op8 ==  1: # ADD R0,N
                return {
                    'op': 'ADD',
                    'args': {'mode':1, 'n':n}
                }
            elif op8 ==  2: # INC RY
                return {
                    'op': 'INC',
                    'args': {'y':y}
                }
            elif op8 ==  3: # DEC RY
                return {
                    'op': 'DEC',
                    'args': {'y':y}
                }
            elif op8 ==  4: # DSZ RY
                return {
                    'op': 'DSZ',
                    'args': {'y':y}
                }
            elif op8 ==  5: # OR R0,N
                return {
                    'op': 'OR',
                    'args': {'mode':1, 'n':n}
                }
            elif op8 ==  6: # AND R0,N
                return {
                    'op': 'AND',
                    'args': {'mode':1, 'n':n}
                }
            elif op8 ==  7: # XOR R0,N
                return {
                    'op': 'XOR',
                    'args': {'mode':1, 'n':n}
                }
            elif op8 ==  8: # EXR N
                return {
                    'op': 'EXR',
                    'args': {'n':n}
                }
            elif op8 ==  9: # BIT RG,M
                return {
                    'op': 'BIT',
                    'args': {'g':g, 'm':m}
                }
            elif op8 ==  10: # BSET RG,M
                return {
                    'op': 'BSET',
                    'args': {'g':g, 'm':m}
                }
            elif op8 ==  11: # BCLR RG,M
                return {
                    'op': 'BCLR',
                    'args': {'g':g, 'm':m}
                }
            elif op8 ==  12: # BTG RG,M
                return {
                    'op': 'BTG',
                    'args': {'g':g, 'm':m}
                }
            elif op8 ==  13: # RRC RY
                return {
                    'op': 'RRC',
                    'args': {'y':y}
                }
            elif op8 ==  14: # RET R0,N
                return {
                    'op': 'RET',
                    'args': {'n':n}
                }
            elif op8 ==  15: # SKIP F,M
                return {
                    'op': 'SKIP',
                    'args': {'f':f, 'm':m}
                }

    elif mode == "asm":
        ins = instruction.split(" ")
        if len(ins) > 1:
            # we have an instruction in the form [ins, args]
            op = ins[0]
            args = ins[1].split(",")
            nArgs = len(args)
            
            if op ==  'add':
                assert(nArgs==2)
                if args[1][0]=="r":
                    # RX,RY
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'ADD',
                        'args': {'mode':0, 'x':x, 'y':y}
                    }
                else:
                    # R0,N
                    return {
                        'op': 'ADD',
                        'args': {'mode':1, 'n':format(args[1])}
                    }
            elif op ==  'adc':
                # RX,RY
                assert(nArgs==2)
                x = int(args[0][1:])
                y = int(args[1][1:])
                return {
                    'op': 'ADC',
                    'args': {'x':x, 'y':y}
                    }
            elif op ==  'sub':
                # RX,RY
                assert(nArgs==2)
                x = int(args[0][1:])
                y = int(args[1][1:])
                return {
                    'op': 'SUB',
                    'args': {'x':x, 'y':y}
                    }
            elif op ==  'sbb':
                # RX,RY
                assert(nArgs==2)
                x = int(args[0][1:])
                y = int(args[1][1:])
                return {
                    'op': 'SBB',
                    'args': {'x':x, 'y':y}
                    }
            elif op ==  'or':
                assert(nArgs==2)
                if args[1][0]=="r":
                    # RX,RY
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'OR',
                        'args': {'mode':0, 'x':x, 'y':y}
                    }
                else:
                    # R0,N
                    return {
                        'op': 'OR',
                        'args': {'mode':1, 'n':format(args[1])}
                    }
            elif op ==  'and':
                assert(nArgs==2)
                if args[1][0]=="r":
                    # RX,RY
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'AND',
                        'args': {'mode':0, 'x':x, 'y':y}
                    }
                else:
                    # R0,N
                    return {
                        'op': 'AND',
                        'args': {'mode':1, 'n':format(args[1])}
                    }
            elif op ==  'xor':
                assert(nArgs==2)
                if args[1][0]=="r":
                    # RX,RY
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'XOR',
                        'args': {'mode':0, 'x':x, 'y':y}
                    }
                else:
                    # R0,N
                    return {
                        'op': 'XOR',
                        'args': {'mode':1, 'n':format(args[1])}
                    }
            elif op ==  'mov':
                if args[0][0] == 'r' and args[1][0] == 'r':
                    # RX,RY
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'MOV',
                        'args': {'mode':0, 'x':x, 'y':y}
                    }
                elif args[0][0] == '[' and ':' in args[0]:
                    # [X:Y],R0
                    xy = args[0].strip('[]').split(":")
                    x = int(xy[0])
                    y = int(xy[1])
                    return {
                        'op': 'MOV',
                        'args': {'mode':2, 'x':x, 'y':y}
                    }
                elif args[1][0] == '[' and ':' in args[1]:
                    # R0,[X:Y]
                    xy = args[1].strip('[]').split(":")
                    x = int(xy[0])
                    y = int(xy[1])
                    return {
                        'op': 'MOV',
                        'args': {'mode':3, 'x':x, 'y':y}
                    }
                elif args[0][0] == '[':
                    # [NN],R0
                    nn = format(args[0].strip('[]'))
                    return {
                        'op': 'MOV',
                        'args': {'mode':4, 'nn':nn}
                    }
                elif args[1][0] == '[':
                    # R0,[NN]
                    nn = format(args[1].strip('[]'))
                    return {
                        'op': 'MOV',
                        'args': {'mode':5, 'nn':nn}
                    }
                elif args[0][0] == 'r':
                    # RX,N
                    x = int(args[0][1:])
                    return {
                        'op': 'MOV',
                        'args': {'mode':1, 'x':x, 'n':format(args[1])}
                    }
                elif args[0] == 'pc':
                    # PC,NN
                    return {
                        'op': 'MOV',
                        'args': {'mode':6, 'nn':format(args[1])}
                    }
            elif op ==  'jr':
                # NN
                assert(nArgs==1)
                return {
                    'op': 'JR',
                    'args': {'nn':format(args[0])}
                    }
            elif op ==  'cp':
                # R0,N
                assert(nArgs==2)
                return {
                    'op': 'CP',
                    'args': {'n':format(args[0])}
                    }
            elif op ==  'inc':
                # R0,N
                assert(nArgs==1)
                y = int(args[0][1:])
                return {
                    'op': 'INC',
                    'args': {'y':y}
                    }
            elif op ==  'dec':
                # R0,N
                assert(nArgs==1)
                y = int(args[0][1:])
                return {
                    'op': 'DEC',
                    'args': {'y':y}
                    }
            elif op ==  'dsz':
                # RY
                assert(nArgs==1)
                y = int(args[0][1:])
                return {
                    'op': 'DSZ',
                    'args': {'y':y}
                    }
            elif op ==  'exr':
                # N
                assert(nArgs==1)
                return {
                    'op': 'EXR',
                    'args': {'n':format(args[0])}
                    }
            elif op ==  'bit':
                # RG,M
                assert(nArgs==2)
                g = int(args[0][1:])
                m = format(args[1])
                return {
                    'op': 'BIT',
                    'args': {'g':g, 'm':m}
                }
            elif op ==  'bset':
                # RG,M
                assert(nArgs==2)
                g = int(args[0][1:])
                m = format(args[1])
                return {
                    'op': 'BSET',
                    'args': {'g':g, 'm':m}
                }
            elif op ==  'bclr':
                # RG,M
                assert(nArgs==2)
                g = int(args[0][1:])
                m = format(args[1])
                return {
                    'op': 'BCLR',
                    'args': {'g':g, 'm':m}
                }
            elif op ==  'btg':
                # RG,M
                assert(nArgs==2)
                g = int(args[0][1:])
                m = format(args[1])
                return {
                    'op': 'BTG',
                    'args': {'g':g, 'm':m}
                }
            elif op ==  'rrc':
                # RY
                assert(nArgs==1)
                y = int(args[0][1:])
                return {
                    'op': 'RRC',
                    'args': {'y':y}
                }
            elif op ==  'ret':
                # R0,N
                assert(nArgs==2)
                n = format(args[1])
                return {
                    'op': 'RET',
                    'args': {'n':n}
                }
            elif op ==  'skip':
                #F,M
                return {
                    'op': 'SKIP',
                    'args': {'f':format(args[0]), 'm':format(args[1])}
                }
    
    return None



