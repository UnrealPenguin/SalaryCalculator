from tkinter import *
import Constants as c
import pandas as pd
from pandastable import Table

from data.getGspread import getGspread
from data.processData import processData
from data.addEmployeeID import addEmployeeID

class Display():
    def __init__(self, parent, width, height):
        self.parent = parent ### parent is root

        # configure the window
        self.parent.title(c.NAME)        
        self.parent.configure(bg=c.BGCOLOR)

        container = Frame(parent, width=width, height=height, bg=c.BGCOLOR)
        container.pack()

        title = Label(container, text=c.NAME, bg=c.BGCOLOR, fg="white", font=(None, 32))
        title.place(x=10, y=10)

        step1 = Label(container, text="Step 1", bg=c.BGCOLOR, fg="white", font=(None, 18))
        step1.place(x=50, y=100)

        step1description = Label(container, 
                                text="Insert google spreadsheet link. (Does not take .xls or .xlsx) If .xls or xlsx format, Import it in google spreadsheet to convert correct format.",
                                bg=c.BGCOLOR, fg="white")
        step1description.place(x=50, y=150)     

        # FOR ATTENDANCE DATA
        attendanceLabel = Label(container, text="Attendance Link:", bg=c.BGCOLOR, fg="white")
        self.attendanceInput = Entry(container)
        attendanceLabel.place(x=50, y=200)
        self.attendanceInput.place(x=170, y=200)

        # FOR TAX DATA
        taxLabel = Label(container, text="Tax Link:", bg=c.BGCOLOR, fg="white")
        self.taxInput = Entry(container)
        taxLabel.place(x=50, y=230)
        self.taxInput.place(x=170, y=230)

        # FOR EXCEPTIONS
        step2 = Label(container, text="Step 2", bg=c.BGCOLOR, fg="white", font=(None, 18))
        step2.place(x=50, y=280)

        step2description = Label(container, 
                                text="Insert which day of the month is an exception. Seperate each date with a comma (i.e. 20, 23 for 20th and 23rd)",
                                bg=c.BGCOLOR, fg="white")
        step2description.place(x=50, y=330)

        # FOR DAY OFF EXCEPTION
        dayOffLabel = Label(container, text="Day Off:", bg=c.BGCOLOR, fg="white")
        self.dayOffInput = Entry(container)
        dayOffLabel.place(x=50, y=380)
        self.dayOffInput.place(x=170, y=380)

        # FOR HOLIDAY EXCEPTION
        holidayLabel = Label(container, text="Holiday:", bg=c.BGCOLOR, fg="white")
        self.holidayInput = Entry(container)
        holidayLabel.place(x=50, y=410)
        self.holidayInput.place(x=170, y=410)

        # FOR DISPLAYING THE NEW DF ON CLICK
        btnCalculate = Button(container, text="Calculate Salary", command=self.displayDF)
        btnCalculate.place(x=750, y=650)


    def getData(self):
        # retrieve link from the input box
        attendanceLink = self.attendanceInput.get()
        taxLink = self.taxInput.get()

        attendance = getGspread()
        attendance = attendance.getSpreadSheet(attendanceLink)
        attendance = attendance.worksheet("考勤记录")

        tax = getGspread()
        tax = tax.getSpreadSheet(taxLink)
        tax = tax.sheet1
        # Adds Employee ID to tax sheet to cross reference both spreadsheet
        addEmployeeID(tax)

        process = processData(attendance, tax)

        # Checks if there's exceptions
        exception = []
        dayOffDate = self.dayOffInput.get()
        holidayDate = self.holidayInput.get()

        if(dayOffDate):
            dayOffs = dayOffDate.replace(" ", "").split(",")
            exception.extend(process.createExceptions(dayOffs, 0))

        if(holidayDate):
            holiday = holidayDate.replace(" ", "").split(",")
            exception.extend(process.createExceptions(holiday, 1))

        process.calculateAttendance(exception)

        data = []
        for employee in process.getAllEmployees():

            data.append(
                {
                    "ID": employee.getId(),
                    "Name": employee.getName(),
                    "NORMAL HOURS" : "",
                    "Days worked": employee.getDaysWorked(),
                    "OVERTIME HOURS" : "",
                    "Overtime (hours)": employee.getOTworked(),

                    "LATE TIMES" : "",
                    "1-5min": employee.getLate5Min(),
                    "6-10min": employee.getLate10Min(),
                    "11-20min": employee.getLate20Min(),
                    "21-50min": employee.getLate50Min(),
                    "50+min": employee.getLateMax(),

                    "EARLY TIMES" : "",
                    "1-5 min": employee.getEarly5Min(),
                    "6-10 min": employee.getEarly10Min(),
                    "11-20 min": employee.getEarly20Min(),
                    "21-50 min": employee.getEarly50Min(),
                    "50+ min": employee.getEarlyMax(),
                    
                    " ": "",

                    "EARNING CALCULATIONS": "",
                    "Basic Salary": employee.getTotalBasicSalary(),
                    "Transportation": employee.getTotalTransportation(),
                    "Medical": employee.getTotalMedical(),
                    "Injury": employee.getTotalInjury(),
                    "Lunch": employee.getTotalLunch(),
                    "Position": employee.getTotalPosition(),
                    "Additional lunch": employee.getTotalAddLunch(),
                    "Additional transportation": employee.getTotalAddTransportation(),

                    "Additional Allowance total": employee.getAddAllow(),
                    "SubTotal": employee.getSubTotal(),
                    "SubTotal + Additional Allowance": employee.getSubTotalWithAdd(),

                    "   ": "",

                    "Deductions": employee.getDeductions(),
                    "Income Tax": employee.getIncomeTax(),
                    "Pension": employee.getPension(),
                    "Total Deductions": employee.getTotalDeductions(),

                    "    ": "",

                    "Total Before Bonus": employee.getTotalBeforeBonus(),
                    "Full Attendance": employee.getFullAttend(),
                    "Diploma Bonus": employee.getDiplomaBonus(),
                    "Leadership Bonus": employee.getLeadershipBonus(),
                    "Service Bonus": employee.getServiceBonus(),

                    "TOTAL": employee.getGrandTotal()
                }
            )

        df = pd.DataFrame(data)
        df.set_index("ID", inplace=True)
        # tranpose dataframe
        df = df.T

        return df

    def displayDF(self):
        frame = Toplevel(self.parent)
        self.table = Table(frame, dataframe=self.getData(), showtoolbar=True, showstatusbar=True, maxcellwidth=1500)
        self.table.showindex = True

        # Styling the table
        self.table.setRowColors(rows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], clr="lightblue", cols='all')
        self.table.setRowColors(rows=[18, 19,20,21,22,23,24,25,26,27,28,29], clr="lightgreen", cols='all')
        self.table.setRowColors(rows=[31,32,33], clr="#EF6E6E", cols='all')
        self.table.setRowColors(rows=34, clr="#E24141", cols='all')
        self.table.setRowColors(rows=36, clr="#58D337", cols='all')
        self.table.setRowColors(rows=[37,38,39,40], clr="#F7F98E", cols='all')
        self.table.setRowColors(rows=41, clr="#CCC72B", cols='all')

        self.table.show()



        