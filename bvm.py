# bvm.py
# Adam Zeloof
# 3.12.2022
# requires Python 3.10 or higher

from bvmParser import parse
from bvmCPU import CPU

class BVM:
    def __init__(self):
        self.progMem = []
        self.cpu = CPU()

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
        print(self.cpu.ram[0:16])

    def run(self):
        while self.cpu.getPC() < len(self.progMem):
            self.step()


if __name__ == "__main__":
    bvm = BVM()
    bvm.load('program.bvm')
    print(bvm.progMem)
    bvm.run()
    #bvm.step()
    #bvm.step()
    #bvm.step()
