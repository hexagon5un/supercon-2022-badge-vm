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
            match op4:
                case 1: # ADD RX,RY
                    return {
                        'op': 'ADD',
                        'args': {'mode':0, 'x':x, 'y':y}
                        }
                case 2: # ADC RX,RY
                    return {
                        'op': 'ADC',
                        'args': {'x':x, 'y':y}
                        }
                case 3: # SUB RX,RY
                    return {
                        'op': 'SUB',
                        'args': {'x':x, 'y':y}
                        }
                case 4: # SBB RX,RY
                    return {
                        'op': 'SBB',
                        'args': {'x':x, 'y':y}
                        }
                case 5: # OR RX,RY
                    return {
                        'op': 'OR',
                        'args': {'mode':0, 'x':x, 'y':y}
                        }
                case 6: # AND RX,RY
                    return {
                        'op': 'AND',
                        'args': {'mode':0, 'x':x, 'y':y}
                        }
                case 7: # XOR RX,RY
                    return {
                        'op': 'XOR',
                        'args': {'mode':0, 'x':x, 'y':y}
                        }
                case 8: # MOV RX,RY
                    return {
                        'op': 'MOV',
                        'args': {'mode':0, 'x':x, 'y':y}
                        }
                case 9: # MOV RX,N
                    return {
                        'op': 'MOV',
                        'args': {'mode':1, 'x':x, 'n':n}
                        }
                case 10: # MOV [XY],R0
                    return {
                        'op': 'MOV',
                        'args': {'mode':2, 'x':x, 'y':y}
                        }
                case 11: # MOV R0,[XY]
                    return {
                        'op': 'MOV',
                        'args': {'mode':3, 'x':x, 'y':y}
                        }
                case 12: # MOV [NN],R0
                    return {
                        'op': 'MOV',
                        'args': {'mode':4, 'nn':nn}
                        }
                case 13: # MOV R0,[NN]
                    return {
                        'op': 'MOV',
                        'args': {'mode':5, 'nn':nn}
                        }
                case 14: # MOV PC,NN
                    return {
                        'op': 'MOV',
                        'args': {'mode':6, 'nn':nn}
                        }
                case 15: # JR NN
                    return {
                        'op': 'JR',
                        'args': {'nn':nn}
                        }
        else:
            # We have an eight-bit opcode
            match op8:
                case 0: # CP R0,N
                    return {
                        'op': 'CP',
                        'args': {'n':n}
                    }
                case 1: # ADD R0,N
                    return {
                        'op': 'ADD',
                        'args': {'mode':1, 'n':n}
                    }
                case 2: # INC RY
                    return {
                        'op': 'INC',
                        'args': {'y':y}
                    }
                case 3: # DEC RY
                    return {
                        'op': 'DEC',
                        'args': {'y':y}
                    }
                case 4: # DSZ RY
                    return {
                        'op': 'DSZ',
                        'args': {'y':y}
                    }
                case 5: # OR R0,N
                    return {
                        'op': 'OR',
                        'args': {'mode':1, 'n':n}
                    }
                case 6: # AND R0,N
                    return {
                        'op': 'AND',
                        'args': {'mode':1, 'n':n}
                    }
                case 7: # XOR R0,N
                    return {
                        'op': 'XOR',
                        'args': {'mode':1, 'n':n}
                    }
                case 8: # EXR N
                    return {
                        'op': 'EXR',
                        'args': {'n':n}
                    }
                case 9: # BIT RG,M
                    return {
                        'op': 'BIT',
                        'args': {'g':g, 'm':m}
                    }
                case 10: # BSET RG,M
                    return {
                        'op': 'BSET',
                        'args': {'g':g, 'm':m}
                    }
                case 11: # BCLR RG,M
                    return {
                        'op': 'BCLR',
                        'args': {'g':g, 'm':m}
                    }
                case 12: # BTG RG,M
                    return {
                        'op': 'BTG',
                        'args': {'g':g, 'm':m}
                    }
                case 13: # RRC RY
                    return {
                        'op': 'RRC',
                        'args': {'y':y}
                    }
                case 14: # RET R0,N
                    return {
                        'op': 'RET',
                        'args': {'n':n}
                    }
                case 15: # SKIP F,M
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
            match op:
                case 'add':
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
                case 'adc':
                    # RX,RY
                    assert(nArgs==2)
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'ADC',
                        'args': {'x':x, 'y':y}
                        }
                case 'sub':
                    # RX,RY
                    assert(nArgs==2)
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'SUB',
                        'args': {'x':x, 'y':y}
                        }
                case 'sbb':
                    # RX,RY
                    assert(nArgs==2)
                    x = int(args[0][1:])
                    y = int(args[1][1:])
                    return {
                        'op': 'SBB',
                        'args': {'x':x, 'y':y}
                        }
                case 'or':
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
                case 'and':
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
                case 'xor':
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
                case 'mov':
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
                case 'jr':
                    # NN
                    assert(nArgs==1)
                    return {
                        'op': 'JR',
                        'args': {'nn':format(args[0])}
                        }
                case 'cp':
                    # R0,N
                    assert(nArgs==2)
                    return {
                        'op': 'CP',
                        'args': {'n':format(args[0])}
                        }
                case 'inc':
                    # R0,N
                    assert(nArgs==2)
                    return {
                        'op': 'INC',
                        'args': {'n':format(args[0])}
                        }
                case 'dec':
                    # R0,N
                    assert(nArgs==2)
                    return {
                        'op': 'DEC',
                        'args': {'n':format(args[0])}
                        }
                case 'dsz':
                    # R0,N
                    assert(nArgs==2)
                    return {
                        'op': 'DSZ',
                        'args': {'n':format(args[0])}
                        }
                case 'exr':
                    # N
                    assert(nArgs==1)
                    return {
                        'op': 'EXR',
                        'args': {'n':format(args[0])}
                        }
                case 'bit':
                    # RG,M
                    assert(nArgs==2)
                    g = format(args[0][1:])
                    m = format(args[1])
                    return {
                        'op': 'BIT',
                        'args': {'g':g, 'm':m}
                    }
                case 'bset':
                    # RG,M
                    assert(nArgs==2)
                    g = int(args[0][1:])
                    m = format(args[1])
                    return {
                        'op': 'BSET',
                        'args': {'g':g, 'm':m}
                    }
                case 'bclr':
                    # RG,M
                    assert(nArgs==2)
                    g = int(args[0][1:])
                    m = format(args[1])
                    return {
                        'op': 'BCLR',
                        'args': {'g':g, 'm':m}
                    }
                case 'btg':
                    # RG,M
                    assert(nArgs==2)
                    g = int(args[0][1:])
                    m = format(args[1])
                    return {
                        'op': 'BTG',
                        'args': {'g':g, 'm':m}
                    }
                case 'rrc':
                    # RY
                    assert(nArgs==1)
                    y = int(args[0][1:])
                    return {
                        'op': 'RRC',
                        'args': {'y':y}
                    }
                case 'ret':
                    # R0,N
                    assert(nArgs==2)
                    n = format(args[1])
                    return {
                        'op': 'RET',
                        'args': {'n':n}
                    }
                case 'skip':
                    #F,M
                    return {
                        'op': 'SKIP',
                        'args': {'f':format(args[0]), 'm':format(args[1])}
                    }
                    
    
    return None



