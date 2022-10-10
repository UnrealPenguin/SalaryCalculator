from tkinter import *
from Display import Display
import constants as c

from data.addEmployeeID import addEmployeeID

# --------- MOVE TO DISPLAY WHEN IMPLEMENTED
from data.getGspread import getGspread
from data.processData import processData

attendance = getGspread()
attendance = attendance.getSpreadSheet("https://docs.google.com/spreadsheets/d/1pPt4M50dhPWkGLJKGGBO-msXP4grRbQvk8n_CTx0qBQ/edit#gid=429097067")
attendance = attendance.worksheet("考勤记录")

tax = getGspread()
tax = tax.getSpreadSheet("https://docs.google.com/spreadsheets/d/1_spV2ckju7dzL_OtL3ocT8tYkQSgi1-TJOsIiQi-sek/edit#gid=1604391784")
tax = tax.sheet1

# Adds Employee ID to tax sheet to cross reference both spreadsheet
addEmployeeID(tax)

process = processData(attendance, tax)

exception = [{"date":10, "exception":"dayOff"}, {"date":12,"exception":"dayOff"}, {"date":13,"exception":"dayOff"}]
# note-to-self if not empty append, else create the array
exception.extend([{"date":27, "exception":"dayOff"}, {"date":28, "exception":"dayOff"}])
exception.extend([{"date":26, "exception":"hourly"}, {"date":29, "exception":"hourly"}, {"date":30, "exception":"hourly"}])

process.calculateAttendance(exception)

# --------- MOVE TO DISPLAY WHEN IMPLEMENTED

root = Tk()
Display(root, c.WIDTH, c.HEIGHT)

root.mainloop()