# bvmGUI.py
# Adam Zeloof
# 9.13.2022
# requires Python 3.10 or higher

from bvmCPU import CPU

import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self):
        self.cpu = CPU()
        self.width = 1594
        self.height = 857
        self.window = tk.Tk()
        self.window.title("BVM: 2022 Hackaday Supercon Badge Virtual Machine")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bd=0)
        bg = Image.open("gui_assets/badgeface.png")
        bg.thumbnail((self.width, self.height), Image.ANTIALIAS)
        self.bgImage = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bgImage)
        self.canvas.pack()

    def run(self):
        self.window.mainloop()


class LED:
    def __init__(self, x, y, theta, color):
        self.x = x
        self.y = y
        self.theta = theta
        self.color = color
        self.val = 0


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y


        