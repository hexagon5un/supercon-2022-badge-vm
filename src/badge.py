# badge.py
# Adam Zeloof
# 9.14.2022
# requires Python 3.10 or higher

from bvmCPU import CPU
from bvmParser import parse

class Badge():
    def __init__(self):
        self.cpu = CPU()
        self.progMem = []
        self.pc = 0
        self.acc = [
            0b0000, # lower
            0b0000, # middle
            0b0000  # upper
        ]
        self.cFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.zFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.vFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.userCarry = 0b0
        self.adders = [
            0b0000, # dest bits
            0b0000, # source bits
            0b0000, # carry bits
            0b0000  # sum bits
        ]
        self.page = 0b0000


    def load(self, program):
        with open(program) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(" ","")
                line = line.split('//')[0]
                if line != '':
                    self.progMem.append(int(line,2))


    def step(self):
        instruction = parse(self.progMem[self.cpu.getPC()])
        if instruction is not None:
            getattr(self.cpu, instruction['op'])(instruction['args'])
        self.cpu.step()
