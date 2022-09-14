# bvm.py
# Adam Zeloof
# 3.12.2022
# requires Python 3.10 or higher

from bvmParser import parse
from bvmCPU import CPU
from bvmGUI import GUI

import sys
import getopt

class BVM:
    def __init__(self, inputMode):
        self.progMem = []
        self.cpu = CPU()
        self.inputMode = inputMode

    def load(self, program):
        if program is not None:
            with open(program) as f:
                lines = f.readlines()
                for line in lines:
                    #line = line.replace(" ","")
                    line = line.replace("\n","")
                    line = line.split('//')[0]
                    if line != '':
                        self.progMem.append(line)

    def step(self):
        instruction = parse(self.progMem[self.cpu.getPC()], self.inputMode)
        #print(instruction)
        if instruction is not None:
            getattr(self.cpu, instruction['op'])(instruction['args'])
        self.cpu.step()
        # Print out the first 16 registers (R0-R15) on each step
        print(self.cpu.ram[0:16])

    def run(self):
        while self.cpu.getPC() < len(self.progMem):
            self.step()


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"tbi:",['input='])
    except getopt.GetoptError:
        print("bvm.py [-t] [-b] [-i] filename.bvm")
        sys.exit(2)
        
    guiMode = True
    inputMode = "asm"
    inFile = None

    for opt, arg in opts:
        if opt == '-t':
            guiMode = False
        if opt == '-b':
            inputMode = "bin"
        if opt == '-i':
            inFile = arg

    if guiMode:
        gui = GUI(inputMode)
        gui.load(inFile)
        gui.run()
    else:
        # No GUI, run program.bvm
        bvm = BVM(inputMode)
        bvm.load(inFile)
        bvm.run()


if __name__ == "__main__":
    main(sys.argv[1:])