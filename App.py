from tkinter import *
from Display import Display
import constants as c

root = Tk()
Display(root, c.WIDTH, c.HEIGHT)

root.mainloop()

# If only a single punch is present -> employee has not worked that day
