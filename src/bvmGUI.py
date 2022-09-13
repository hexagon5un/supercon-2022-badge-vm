# bvmGUI.py
# Adam Zeloof
# 9.13.2022
# requires Python 3.10 or higher

from optparse import OptionConflictError
from bvmCPU import CPU

import tkinter as tk
from PIL import Image, ImageTk
import csv
import math

class GUI:
    def __init__(self):
        self.cpu = CPU()
        self.width = 1408
        self.height = 776
        self.window = tk.Tk()
        self.window.title("BVM: 2022 Hackaday Supercon Badge Virtual Machine")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bd=0)
        bg = Image.open("gui_assets/badgeface.png")
        bg.thumbnail((self.width, self.height), Image.ANTIALIAS)
        self.bgImage = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bgImage)
        self.canvas.pack()
        self.redLeds = []
        self.yellowLeds = []
        self.buttons = []
        self.parsePnp()
        self.redLeds.sort()
        self.yellowLeds.sort()

    def run(self):
        self.window.mainloop()

    def parsePnp(self):
        # pcb width 174.955 mm    2701 px      15.44 px/mm    /2=7.72
        scale = 7.75
        x0 = 31
        y0 = 21
        with open("gui_assets/pnp.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            for row in reader:
                if len(row) > 9:
                    elmId = row[0]
                    x = float(row[2][:-2])*scale+x0
                    y = self.height-(float(row[3][:-2])*scale+y0)
                    theta = float(row[9])
                    if elmId[0:2] == "LR":
                        num = int(elmId[3:])
                        self.redLeds += [LED(num, x, y, theta, "red", self.canvas)]
                    elif elmId[0:2] == "LY":  
                        num = int(elmId[3:])
                        self.yellowLeds += [LED(num, x, y, theta, "yellow", self.canvas)]
                    elif elmId[0:2] == "SW":
                        self.buttons += [Button(x, y, self.canvas)]


class LED:
    def __init__(self, num, x, y, theta, color, canvas):
        self.w = 20
        self.h = 10
        self.x = x
        self.y = y
        self.num = num
        self.theta = -math.radians(theta)
        self.color = color
        if self.color == "red":
            self.offColor = "#400"
            self.onColor = "red"
        elif self.color == "yellow":
            self.offColor = "#440"
            self.onColor = "yellow"
        else:
            # This should never happen
            self.offColor = "blue"
            self.onColor = "blue"
        self.canvas = canvas
        self.val = 0
        self.draw()

    def __lt__(self, other):
        return self.num < other.num

    def __repr__(self):
        return str(self.num)

    def draw(self):
        x0 = self.x+(-self.w*math.cos(self.theta)/2+self.h*math.sin(self.theta)/2)
        y0 = self.y+(-self.h*math.cos(self.theta)/2-self.w*math.sin(self.theta)/2)
        x1 = self.x+(-self.w*math.cos(self.theta)/2-self.h*math.sin(self.theta)/2)
        y1 = self.y+(self.h*math.cos(self.theta)/2-self.w*math.sin(self.theta)/2)
        x2 = self.x+(self.w*math.cos(self.theta)/2-self.h*math.sin(self.theta)/2)
        y2 = self.y+(self.h*math.cos(self.theta)/2+self.w*math.sin(self.theta)/2)
        x3 = self.x+(self.w*math.cos(self.theta)/2+self.h*math.sin(self.theta)/2)
        y3 = self.y+(-self.h*math.cos(self.theta)/2+self.w*math.sin(self.theta)/2)
        self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill=self.offColor)

##################### LED Map #####################
# Red LEDs:
# 1-128: Matrix (left-right, top-bottom)
# 129: ADDER 3 Cout
# 130: ADDER 3 Cin
# 131: ADDER 2 Cin
# 132: ADDER 1 Cin
# 133: ADDER 3 SUM
# 134: ADDER 2 SUM
# 135: ADDER 1 SUM
# 136: ADDER 0 SUM
# 137: ACC3 IN
# 138: ACC2 IN
# 139: ACC1 IN
# 140: ACC0 IN
# 141: ACC3 TMP
# 142: ACC2 TMP
# 143: ACC1 TMP
# 144: ACC0 TMP
# 145: ACC3 OUT
# 146: ACC2 OUT
# 147: ACC1 OUT
# 148: ACC0 OUT
# 149: CLK
# 150: CLK Inverter
# 151: N (Next to EXR)
# 152: Carry Input Logic CIN (Cin ENA)
# 153: Carry Inpput Logic INV (DATA INV)
# 154: PG 3
# 155: PG 2
# 156: PG 1
# 157: MODE DIR
# 158: MODE SS
# 159: MODE RUN
# 160: MODE PGM
# 161: CARRY
# 162: SAVE
# 163: LOAD
# 164: CLOCK
# 165: OPCODE 8
# 166: OPCODE 4
# 167: OPCODE 2
# 168: OPCODE 1
# 169: OPERAND X 8
# 170: OPERAND X 4
# 171: OPERAND X 2
# 172: OPERAND X 1
# 173: OPERAND Y 8
# 174: OPERAND Y 4
# 175: OPERAND Y 2
# 176: OPERAND Y 1
# 177: DATA IN BIN
# 178: DATA IN SEL
# 179: ADDER 0 Cin
# 180: SP 2
# 181: SP 1
# 182: SP 0
# 183: PG 0
#
#
# Yellow LEDs:
# 1-16: OPERAND Y 0-15
# 17-32: OPERAND X 0-15
# 33-48: OPCODE 0-15
# 49: ADDER 0 DEST
# 50: ADDER 1 DEST
# 51: ADDER 2 DEST
# 52: ADDER 3 DEST
# 53: ADDER 0 SRC
# 54: ADDER 1 SRC
# 55: ADDER 2 SRC
# 56: ADDER 3 SRC
# 57: LOGIC 0 OR
# 58: LOGIC 1 OR
# 59: LOGIC 2 OR
# 60: LOGIC 3 OR
# 61: LOGIC 0 AND
# 62: LOGIC 1 AND
# 63: LOGIC 2 AND
# 64: LOGIC 3 AND
# 65: LOGIC 0 XOR
# 66: LOGIC 1 XOR
# 67: LOGIC 2 XOR
# 68: LOGIC 3 XOR
# 69: C IN
# 70: Z IN
# 71: V IN
# 72: V TMP
# 73: Z TMP
# 74: C TMP
# 75: V OUT
# 76: Z OUT
# 77: C OUT
# 78: PC 3
# 79: PC 2
# 80: PC 1
# 81: PC 0
# 82: PC 11
# 83: PC 10
# 84: PC 9
# 85: PC 8
# 86: PC 7
# 87: PC 6
# 88: PC 5
# 89: PC 4
###################################################


class Button:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y


        