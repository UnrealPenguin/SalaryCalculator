
from datetime import date, datetime, timedelta

class processData:
    def __init__(self, _sheet):
        self.sheet = _sheet
        # Retrieve all data from spreadsheet
        self.record = self.sheet.get_all_values()
        # Month start
        self.date = self.sheet.acell('C3').value.split("~")[0].strip()
        self.startFrom = datetime.strptime(self.date, "%Y-%m-%d")

        # All currency denoted in Birr
        self.overtimeRate = 5.625 
        
        # Basic salary given every work day 
        daily = 30
        medical = 4
        injury = 4
        transportation = 8 + 5
        lunch = 25 + 5

        self.basicSalary = daily+medical+injury+transportation+lunch
         
    # produces a tuple of : the name (String), 
    #                       total hours worked (Int), 
    #                       full attendance (Bool) of an employee
    def calculateAttendance(self, _exceptions):

        # Check if there are any exceptions this month
        if(_exceptions):
            for i in range(len(_exceptions)):
                # converts date to datetime
                exceptionDate =  datetime.strptime(self.date[:-2]+str(_exceptions[i]["date"]), "%Y-%m-%d")
                _exceptions[i]["date"] = exceptionDate

        # Start from 8th index everything before is useless
        # Iterate by 2 since each row is a data pair
        # CHANGE BACK TO LEN(RECORD)
        for i in range(8, 10, 2):
            
            if(self.isWorking(self.record[i+1])):
                # 9th element is always going to be the name
                name = self.record[i][10]
                self.checkRecord(self.record[i+1], _exceptions)
                # create employee here (?)

        # IGNORE DERIBER (special case)

    # Array -> Bool
    # Given employee list ignores all non working employees in the spreadsheet
    def isWorking(self, _record):
        return False if not any(s.strip() for s in _record) else True
    
    # Array Array -> Int
    # Given employee list calculate his total hours worked
    def checkRecord(self, _record, _exceptions):   

        date = self.startFrom     
        # by default, every employee has full attendance unless missing one day or late/early leave more than 4 hours
        late = 0
        earlyLeave = 0
        absentDays = 0
        daysWorked = 0
        fullAttendance = True

        for i in range(len(_record)):

            # If there are exceptions
            hasException, j = self.isException(_exceptions, date)
            if(hasException):
                # if exception is a holiday
                if(_exceptions[j]["exception"] == "holiday"):
                    # remove from exception array after usage
                    del _exceptions[j] 
                # if exception is a company day off
                elif(_exceptions[j]["exception"] == "dayOff"):              
                    # remove from exception array after usage
                    del _exceptions[j] 
                #  if exception is hourly pay
                else:
                    del _exceptions[j] 
            else:
                # normal work day calculation
                self.normalDay(date, _record[i])
            
            # increment date by 1 after each loop
            date += timedelta(days=1)
        print(absentDays)
    
    # Dict, Datetime -> Bool, index
    # Given a dict and a date produces true and current index if the date matches the exception date 
    # False otherwise
    def isException(self, _exceptions, _date):
        if(_exceptions):
            for j in range(len(_exceptions)):
                if(_date == _exceptions[j]["date"]):
                    # print(_date)
                    return True, j
            # return False only if none of the date matches
            return False, 0
        else:
            return False, 0

    # Date Array -> Int Int
    # produces the amount earned (in Birr) on a normal workday 
    def normalDay(self, _date, _record):
        absentCount = 0
        workedDay = 0

        # Checks what day of the week it is, if worked on sunday extra pay
        # 0 = monday, 6 = sunday
        if(_date.weekday() != 6):
            if(not _record):
                print(_date)
                absentCount += 1
            else:
                self.processTime(_record)
                workedDay += 1
                # hoursWorked = punchTimes[len(punchTimes)-1]- punchTimes[0]
                # print(hoursWorked)
        
        return workedDay, absentCount

    def processTime(self, _record):
        startTime = datetime.strptime("07:00", "%H:%M")
        endTime = datetime.strptime("17:30", "%H:%M")

        overtime = datetime.strptime("18:00", "%H:%M")
        punchIn = 0
        punchOut = 0

        # Get the first and last punch in times from the record
        # if punched in before startTime -> round to startTime
        # if punch out after endTime -> round to EndTime
        if(datetime.strptime(_record[0:5], "%H:%M") < startTime):
            punchIn = startTime
        else:
            # late
            pass
        if(datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") > endTime and
            datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") < overtime):
            punchOut = endTime
        elif():
            # early leave
            pass
        else:
            # if working past 18:00 means overtime. Take the latest punch out time
            punchOut = datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") 

        # calculate total overtime worked
        overtimePay = (punchOut-punchIn) - timedelta(hours=8)
        # get time in int
        overtimePay = overtimePay.seconds/3600
        overtimePay = overtimePay*self.overtimeRate
        print(overtimePay)

    # -> Int
    # produces the amount earned (in Birr) on a day off for employees who work 
    # prevents other employees to lose full attendance if not working on this particular day
    def dayOff(self):
        pass
    # -> Int
    # produces the amount earned (in Birr) on a holiday for employees who work 
    # prevents other employees to lose full attendance if not working on this particular day
    def holiday(self):
        pass
