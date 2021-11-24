from tkinter import *
import winsound

class LaunchWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Tank Game Launcher')
        self.geometry('1280x720+0+0')
        self.config(bg='White')
        #self.iconbitmap('assets//jack.ico')
