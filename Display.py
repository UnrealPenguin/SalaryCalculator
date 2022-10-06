from tkinter import *

class Display():
    def __init__(self, parent, width, height):
        self.parent = parent ### parent is root
        self.container = Frame(parent)
