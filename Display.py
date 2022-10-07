from tkinter import *
import constants as c

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
                                text="Insert google spreadsheet link. (Does not take .xls or .xlsx) If .xls or xlsx format, Import it Gspread to convert to google spreadsheet format.",
                                bg=c.BGCOLOR, fg="white")
        step1description.place(x=50, y=150)
                        

        # FOR ATTENDANCE DATA
        attendanceLabel = Label(container, text="Attendance Link:", bg=c.BGCOLOR, fg="white")
        self.attendanceInput = Entry(container)
        attendanceLabel.place(x=50, y=200)
        self.attendanceInput.place(x=145, y=200)

        # FOR TAX DATA
        taxLabel = Label(container, text="Tax Link:", bg=c.BGCOLOR, fg="white")
        self.taxInput = Entry(container)
        taxLabel.place(x=50, y=230)
        self.taxInput.place(x=145, y=230)
        # btnAttendance = Button(container, text="Fetch", command=self.getAttendanceRecord)
        # btnAttendance.place(x=275, y=198)

        # FOR EXCEPTIONS
        step2 = Label(container, text="Step 2", bg=c.BGCOLOR, fg="white", font=(None, 18))
        step2.place(x=50, y=280)

        step2description = Label(container, 
                                text="Insert which day of the month is an exception. Seperate each date with a comma (i.e. 20, 23 for 20th and 23rd)",
                                bg=c.BGCOLOR, fg="white")
        step2description.place(x=50, y=330)

        # FOR HOLIDAY EXCEPTION
        holidayLabel = Label(container, text="Day Off:", bg=c.BGCOLOR, fg="white")
        self.holidayInput = Entry(container)
        holidayLabel.place(x=50, y=380)
        self.holidayInput.place(x=145, y=380)

        # FOR ATTENDANCE DATA
        dayOffLabel = Label(container, text="Holiday:", bg=c.BGCOLOR, fg="white")
        self.dayOffInput = Entry(container)
        dayOffLabel.place(x=50, y=410)
        self.dayOffInput.place(x=145, y=410)

        self.attendanceLink = ""
        self.taxLink = ""
        self.dayOffDate = []
        self.holidayDate = []

    def getAttendanceRecord(self):
        self.attendanceLink = self.attendanceInput.get()
        self.taxLink = self.taxInput.get()
        # to do (array)
        self.dayOffDate = self.dayOffInput.get()
        self.holidayDate = self.holidayInput.get()



        