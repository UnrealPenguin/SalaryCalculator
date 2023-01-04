
from datetime import date, datetime, timedelta
import Constants as c
from Employee import Employee

class processData:
    def __init__(self, _attendanceSheet, _taxSheet):
        # Retrieve attendance data 
        self.record = _attendanceSheet.get_all_values()
        # Retrieve tax data 
        self.taxSheet = _taxSheet
        # get all active employees id number
        self.taxEmployeeId = [id for id in _taxSheet.col_values(15) if id]

        # Month start
        self.date = _attendanceSheet.acell('C3').value.split("~")[0].strip()
        self.startFrom = datetime.strptime(self.date, "%Y-%m-%d")
        daysInMonth = int(_attendanceSheet.acell('C3').value.split("~")[1].strip()[-2:])
        # Basic salary given every work day 
        self.basicSalary = c.DAILY*daysInMonth
  
        self.allEmployees = []
    
    def calculateAttendance(self, _exceptions):
        incomeTax = pension = 0
        # Check if there are any exceptions this month
        if(_exceptions):
            for i in range(len(_exceptions)):
                # converts date to datetime
                exceptionDate =  datetime.strptime(self.date[:-2]+str(_exceptions[i]["date"]), "%Y-%m-%d")
                _exceptions[i]["date"] = exceptionDate

        # Start from 8th index everything before is useless
        # Iterate by 2 since each row is a data pair
        # 16 17 OLANI
        # 8 10 ABAYA
        # 70, 71
        for i in range(8, len(self.record), 2):
            
            # resets on every loop
            diplomaBonus = leadershipBonus = serviceBonus = totalDeductions = totalBeforeBonus = grandTotal =0
            
            if(self.isWorking(self.record[i+1])):
                # 2nd element is employee ID 9th element is the name
                employeeID = self.record[i][2]
                name = self.record[i][10]
                daysWorked, overtimeWorked, additionalAllowance, subTotal, STwithAddAllow, deductions,  fullAttend = self.checkRecord(self.record[i+1], _exceptions)

                try:
                    cellLocation = self.taxSheet.find(employeeID, in_column=15)
                    incomeTax, pension = self.checkTax(cellLocation)
                except AttributeError:
                    # if employee doesnt have an ID yet, no income tax or pension yet
                    incomeTax = pension = 0

                # Add up all deductions
                totalDeductions = incomeTax + pension + deductions

                # remove incomeTax and pension from STwithAddAllow
                totalBeforeBonus = STwithAddAllow - totalDeductions
                
                # Special bonus for employee
                # diploma, service & leadership
                if(employeeID == "3"):
                    serviceBonus = 380
                    leadershipBonus = 1300

                elif(employeeID == "7"):
                    diplomaBonus = 100
                    serviceBonus = 90
                    leadershipBonus = 100

                elif(employeeID == "9"):
                    serviceBonus = 210
                    leadershipBonus = 1100

                elif(employeeID == "10"):
                    serviceBonus = 390
                    leadershipBonus = 800
                
                elif(employeeID == "15"):
                    serviceBonus = 55

                elif(employeeID == "16"):
                    serviceBonus = 55 

                elif(employeeID == "17"):
                    diplomaBonus = 150
                    serviceBonus = 50
                    leadershipBonus = 300

                elif(employeeID == "18"):
                    serviceBonus = 55

                elif(employeeID == "25"):
                    serviceBonus = 30 

                elif(employeeID == "28"):
                    serviceBonus = 30

                elif(employeeID == "30"):
                    serviceBonus = 20

                elif(employeeID == "33"):
                    diplomaBonus = 100
                    leadershipBonus = 300

                elif(employeeID == "41"):
                    leadershipBonus = 300
                
                # check if full attendance is given
                if(fullAttend):
                    attendBonus = 650
                else:
                    attendBonus = 0
                    
                grandTotal = totalBeforeBonus + attendBonus + diplomaBonus + leadershipBonus + serviceBonus 

                # Format the data so it only shows up to 2 decimals
                self.allEmployees.append(Employee(employeeID, name, daysWorked, float("{:.2f}".format(overtimeWorked)), float("{:.2f}".format(additionalAllowance)), float("{:.2f}".format(subTotal)), float("{:.2f}".format(STwithAddAllow)), 
                                                    deductions, incomeTax, pension, totalDeductions, float("{:.2f}".format(totalBeforeBonus)),
                                                    attendBonus, diplomaBonus, leadershipBonus, serviceBonus, float("{:.2f}".format(grandTotal))))
            
    # Array -> Bool
    # Given employee list ignores all non working employees in the spreadsheet
    def isWorking(self, _record):
        return False if not any(s.strip() for s in _record) else True
    
    # Array Array -> Tuple(Int, Float, Float, Float, Float, Float, Bool)
    # Given an employees record and a list of exception(dates) calculate his total hours worked
    def checkRecord(self, _record, _exceptions):   

        date = self.startFrom     
        # by default, every employee has full attendance unless missing one day or late/early leave more than 4 hours
        absentDays = totalWage = totalDeductions = infractionTime = totalAdditional = totalDaysWorked = totalOT = sundayPay = 0
        fullAttendance = True
   
        for i in range(len(_record)):  
            OTpay = absentCount = deductions = totalTime = allowance = OTworked = holidayPay = 0   

            # If there are exceptions
            hasException, j = self.isException(_exceptions, date)
            if(hasException):
                # if exception is a holiday
                if(_exceptions[j]["exception"] == "holiday"):
                    daysWorked, allowance, additionalAllowance, holidayPay = self.holiday(_record[i])
                # if exception is a company day off
                else:              
                    daysWorked, allowance, additionalAllowance, OTpay, OTworked = self.dayOff(_record[i])

            else:
                # normal work day calculation
                daysWorked, allowance, additionalAllowance, OTpay, absentCount, deductions, totalTime, OTworked, sundayPay = self.normalDay(date, _record[i])

            # Time worked
            totalDaysWorked+=daysWorked
            totalOT+= OTworked
        
            # Add up all the calculated data
            totalWage += allowance
            # Wage for working on sundays
            totalWage += sundayPay 
            totalWage += holidayPay
            totalWage += OTpay

            # Additional allowance
            totalAdditional += additionalAllowance

            absentDays += absentCount
            infractionTime += totalTime
            
            totalDeductions += deductions
            
            # increment date by 1 after each loop
            date += timedelta(days=1)

        totalWage += self.basicSalary

        # check if full attendance is given
        if(absentDays >= 1 or infractionTime > 4):
            fullAttendance = False
        
        return totalDaysWorked, totalOT, totalAdditional, totalWage, totalWage+totalAdditional, totalDeductions, fullAttendance


    # Dict, Datetime -> Bool, index
    # Given a dict and a date produces true and current index if the date matches the exception date 
    # False otherwise
    def isException(self, _exceptions, _date):
        if(_exceptions):
            for j in range(len(_exceptions)):
                if(_date == _exceptions[j]["date"]):
                    return True, j
            # return False only if none of the date matches
            return False, 0
        else:
            return False, 0

    # String -> Tuple(Datetime, Int, Int, Int)
    # Given a record produces the timeworked, timeworked hours, late and early leave
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
        # if employee forgot to clock in or clock out

        if(punchOut-punchIn < timedelta(seconds=1)):
            return timedelta(seconds=0), 0, late, earlyLeave
            
        if(datetime.strptime(_record[0:5], "%H:%M") <= startTime):
            punchIn = startTime
        else:
            # late
            late = datetime.strptime(_record[0:5], "%H:%M") - startTime

        if(datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") < endTime ):
            # early leave
            earlyLeave = endTime - datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M")

        elif(datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") >= endTime and
            datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") <= overtime):
            punchOut = endTime
        else:
            # if working past 18:00 means overtime. Take the latest punch out time
            punchOut = datetime.strptime(_record[len(_record)-5:len(_record)], "%H:%M") 

        timeWorked = (punchOut-punchIn)
        timeWorkedHr = timeWorked.seconds/3600

        return timeWorked, timeWorkedHr, late, earlyLeave

    # Date String -> Tuple(Int Int Int Int Int Int Int Int)
    # produces DaysWorked Allowance, additionalAllowance, the amount earned (in Birr) from OT, # of time absent  
    # amount of deductions and totaltime of late and early leave and overtime worked
    def normalDay(self, _date, _record):
        daysWorked = absentCount = allowance = OTpay = late = earlyLeave = deductions = additionalAllowance = OTworked = sundayPay = 0

        # Checks what day of the week it is, if worked on sunday extra pay
        # 0 = monday, 6 = sunday
        if(_date.weekday() != 6):
            if(not _record):
                absentCount += 1
            else:
                # allowance, additionalAllowance, OTpay, late, earlyLeave = self.processTime(_record)
                timeWorked, timeWorkedHr, late , earlyLeave = self.processTime(_record)

                # calculate normal salary
                if(timeWorked < timedelta(hours=8)):
                    allowance = timeWorkedHr*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)

                    # additional allowance
                    additionalAllowance = timeWorkedHr*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)
                else:
                    allowance = 8*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)
                    additionalAllowance = 8*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)

                # calculate total overtime worked if employee has worked more than 8 hours
                if(timeWorked > timedelta(hours=8)):
                    OTworked = timeWorked - timedelta(hours=8)
                    OTworked = OTworked.seconds/3600
                    OTpay = OTworked*c.OVERTIMERATE
                
                # if employee forgot to clock in or out
                if(timeWorkedHr < 1):
                    absentCount += 1
                else:
                    daysWorked += 1
        else:
            # check if worked on sunday, if yes, give higher hourly wage
            if(_record):
                _, timeWorkedHr, *_ = self.processTime(_record)

                sundayPay = timeWorkedHr*c.SUNDAYRATE
                allowance = timeWorkedHr*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)
                additionalAllowance = timeWorkedHr*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)

                if(timeWorkedHr < 1):
                    absentCount += 1
                else:
                    daysWorked += 1

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
 
        return daysWorked, allowance, additionalAllowance, OTpay, absentCount, deductions, totalTime, OTworked, sundayPay


    # String -> Tuple(Int Int Int Int Int)
    # produces the amount earned (in Birr) on a day off for employees who work 
    # prevents other employees to lose full attendance if not working on this particular day
    def dayOff(self, _record):
        dayWorked = allowance = additionalAllowance = OTpay = OTworked = 0
  
        if(_record):
            # ignore all for the time worked
            timeWorked, timeWorkedHr, *_ = self.processTime(_record)

            # calculate normal salary
            if(timeWorked < timedelta(hours=8)):
                allowance = timeWorkedHr*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)
                # additional allowance
                additionalAllowance = timeWorkedHr*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)

            else:
                allowance = 8*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)
                additionalAllowance = 8*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)
  
            # calculate total overtime worked if employee has worked more than 8 hours
            if(timeWorked > timedelta(hours=8)):
                OTworked = timeWorked - timedelta(hours=8)
                OTworked = OTworked.seconds/3600
                OTpay = OTworked*c.OVERTIMERATE

            dayWorked += 1

        return dayWorked, allowance, additionalAllowance, OTpay, OTworked

    # String -> Tuple(Int Int Int Int Int)
    # produces the amount earned (in Birr) on a holiday for employees who work 
    # prevents other employees to lose full attendance if not working on this particular day
    def holiday(self, _record):
        dayWorked = allowance = additionalAllowance = holidayPay = 0

        if(_record):
            # ignore all for the time worked
            _, timeWorkedHr, *_ = self.processTime(_record)

            holidayPay = timeWorkedHr*c.HOLIDAYRATE
            allowance = timeWorkedHr*(c.MEDICAL+c.INJURY+c.TRANSPORTATION+c.LUNCH+c.POSITION)
            additionalAllowance = timeWorkedHr*(c.ADD_LUNCH+c.ADD_TRANSPORTATION)
        
            dayWorked += 1

        return dayWorked, allowance, additionalAllowance, holidayPay

    # Datetime -> Int 
    # Given a time, calculates the amount to deduct in Birr
    def deductions(self, _time):
        toDeduct = 0
        # return if theres no deductions
        if(_time == 0):
            return toDeduct
        elif(_time > timedelta(minutes=0) and _time < timedelta(minutes=6)):
            # 1-5min late, 10 birr deduction
            toDeduct += 10
        elif(_time > timedelta(minutes=5) and _time < timedelta(minutes=11)):
            # 6-10min late, 20 birr deduction
            toDeduct += 20
        elif(_time > timedelta(minutes=10) and _time < timedelta(minutes=21)):
            # 11-20min late, 30 birr deduction
            toDeduct += 30
        elif(_time > timedelta(minutes=20) and _time < timedelta(minutes=51)):
            # 20-50min late, 50 birr deduction
            toDeduct += 50
        else: 
            toDeduct += 70
        return toDeduct

    # Array -> Tuple(Float, Float)
    # Given the tax record returns the income tax and pension
    def checkTax(self, _cellLocation):
        # 9  is income Tax, 10 is pension
        incomeTax = self.taxSheet.cell(_cellLocation.row, 9).value.strip().replace(",","")
        pension = self.taxSheet.cell(_cellLocation.row, 10).value.strip().replace(",","")

        return float(incomeTax), float(pension)

    # returns the list of all the employees
    def getAllEmployees(self):
        return self.allEmployees

    # Array -> dictionnary
    # Given an array of dates produces a dictionnary of exceptions
    # _type 0 is dayoff, 1 is holiday
    def createExceptions(self, _date, _type):
        _tempArr = []
        for i in range(len(_date)):
            if(_type == 0):
                _tempVal = {"date": _date[i], "exception": "dayOff"}

            elif(_type== 1):
                _tempVal = {"date": _date[i], "exception": "holiday"}

            _tempArr.append(_tempVal)

        return _tempArr
