
from datetime import date, datetime, timedelta
import constants as c

class processData:
    def __init__(self, _sheet):
        self.sheet = _sheet
        # Retrieve all data from spreadsheet
        self.record = self.sheet.get_all_values()
        # Month start
        self.date = self.sheet.acell('C3').value.split("~")[0].strip()
        self.startFrom = datetime.strptime(self.date, "%Y-%m-%d")

        # Basic salary given every work day 
        self.basicSalary = c.DAILY+c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH
         
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
        # 16 17 OLANI
        # 8 10 ABAYA
        for i in range(16, 17, 2):
            
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
    
    # Array Array -> Tuple
    # Given an employees record and a list of exception(dates) calculate his total hours worked
    def checkRecord(self, _record, _exceptions):   

        date = self.startFrom     
        # by default, every employee has full attendance unless missing one day or late/early leave more than 4 hours
        absentDays = 0
        totalDaysWorked = 0
        totalWage = 0
        totalDeductions = 0
        infractionTime = 0
        fullAttendance = True

        for i in range(len(_record)):  
            daysWorked = OTpay = absentCount = deductions = totalTime = 0          
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
                daysWorked, OTpay, absentCount, deductions, totalTime = self.normalDay(date, _record[i])
            
            # Add up all the calculated data
            totalDaysWorked += daysWorked
            totalWage += OTpay
            absentDays += absentCount
            totalDeductions += deductions
            infractionTime += totalTime
            # increment date by 1 after each loop
            date += timedelta(days=1)
       
        # check if full attendance is given
        if(absentDays >= 1 or infractionTime > 4):
            fullAttendance = False
        
        if(fullAttendance):
            totalWage += c.FULLATTENDANCE 
        
        totalWage += totalDaysWorked*self.basicSalary
        

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

    # Date Array -> Tuple(Int Int Int Int Int)
    # produces # of days worked, the amount earned (in Birr) from OT, # of time absent  
    # amount of deductions and totaltime of late and early leave
    def normalDay(self, _date, _record):
        absentCount = 0
        workedDay = 0
        OTpay = 0
        late = 0
        earlyLeave = 0
        deductions = 0
        
        # Checks what day of the week it is, if worked on sunday extra pay
        # 0 = monday, 6 = sunday
        if(_date.weekday() != 6):
            if(not _record):
                print(_date)
                absentCount += 1
            else:
                OTpay, late, earlyLeave = self.processTime(_record)
                workedDay += 1

        deductions += self.deductions(late)
        deductions += self.deductions(earlyLeave)

        # converts datetime to int (hours)
        if (late != 0 and earlyLeave !=0):
            totalTime = (late.seconds/3600)+(earlyLeave.seconds/3600)
        elif(late !=0):
            totalTime = (late.seconds/3600)
        elif(earlyLeave !=0):
            totalTime = (earlyLeave.seconds/3600)
        else:
            totalTime= 0


        return workedDay, OTpay, absentCount, deductions, totalTime

    # Array -> Tuple(Int, Int, Int)
    # Given a record produces the overtime pay, late (min), early leave(min) 
    def processTime(self, _record):
        startTime = datetime.strptime("07:00", "%H:%M")
        endTime = datetime.strptime("17:30", "%H:%M")

        overtime = datetime.strptime("18:00", "%H:%M")

        punchIn = datetime.strptime(_record[0:5], "%H:%M")
        punchOut = datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M")

        late = 0
        earlyLeave = 0

        # Get the first and last punch in times from the record
        # if punched in before startTime -> round to startTime
        # if punch out after endTime -> round to EndTime
        if(datetime.strptime(_record[0:5], "%H:%M") <= startTime):
            punchIn = startTime
        else:
            # late
            late = datetime.strptime(_record[0:5], "%H:%M") - startTime

        if(datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") >= endTime and
            datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") <= overtime):
            punchOut = endTime
        elif(datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") < endTime ):
            # early leave
            earlyLeave = endTime - datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M")
        else:
            # if working past 18:00 means overtime. Take the latest punch out time
            punchOut = datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") 

        # calculate total overtime worked
        overtimePay = (punchOut-punchIn) - timedelta(hours=8)
        # get time in int (hours)
        overtimePay = overtimePay.seconds/3600
        overtimePay = overtimePay*c.OVERTIMERATE

        return overtimePay, late, earlyLeave

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

    # Datetime -> Int 
    # Given a time, calculates the amount to deduct in Birr
    def deductions(self, _time):
        toDeduct = 0
        # return if theres no deductions
        if(_time == 0):
            return toDeduct
        elif(_time > timedelta(minutes=1) and _time < timedelta(minutes=5)):
            # 1-5min late, 10 birr deduction
            toDeduct += 10
        elif(_time > timedelta(minutes=5) and _time < timedelta(minutes=10)):
            # 6-10min late, 20 birr deduction
            toDeduct += 20
        elif(_time > timedelta(minutes=10) and _time < timedelta(minutes=20)):
            # 11-20min late, 30 birr deduction
            toDeduct += 30
        elif(_time > timedelta(minutes=20) and _time < timedelta(minutes=50)):
            # 20-50min late, 50 birr deduction
            toDeduct += 50
        else: 
            toDeduct += 70

        return toDeduct