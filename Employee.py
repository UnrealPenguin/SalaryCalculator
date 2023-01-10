class Employee:
    def __init__(   self, _id, _name, _daysWorked, _overtimeWorked, _additionalAllowance, _subTotal, _STwithAddAllow, 
                    _deductions, _incomeTax, _pension, _totalDeductions, _totalBeforeBonus,
                    _fullAttend, _diplomaBonus, _leadershipBonus, _serviceBonus, _grandTotal,
                    _late5min, _late10min, _late20min, _late50min, _lateMax, _early5min, _early10min, _early20min, _early50min, _earlyMax,
                    _totalBasicSalary, _totalTransportation, _totalMedical, _totalInjury, _totalLunch, _totalPosition, _totalAddLunch, _totalAddTransportation,
                    _totalSundayWorked, _totalSundayHours, _totalHolidayWorked, _totalHolidayHours,
                    _late5birr, _late10birr, _late20birr, _late50birr, _lateMaxbirr,
                    _early5birr, _early10birr, _early20birr, _early50birr, _earlyMaxbirr, _totalOTnormal, _totalHolidayPay, _totalSundayPay):

        self.id = _id
        self.name = _name
        self.daysWorked = _daysWorked
        self.OTworked = _overtimeWorked
        self.addAllowance = _additionalAllowance
        self.subtotal = _subTotal
        self.STwithAddAllow = _STwithAddAllow
        self.deductions = _deductions
        self.incomeTax = _incomeTax
        self.pension = _pension
        self.totalDeductions = _totalDeductions
        self.totalBeforeBonus = _totalBeforeBonus
        self.fullAttend = _fullAttend
        self.diplomaBonus = _diplomaBonus
        self.leadershipBonus = _leadershipBonus
        self.serviceBonus = _serviceBonus
        self.grandTotal = _grandTotal
        self.late5min = _late5min
        self.late10min = _late10min
        self.late20min = _late20min
        self.late50min = _late50min
        self.lateMax = _lateMax
        self.early5min = _early5min
        self.early10min = _early10min
        self.early20min = _early20min
        self.early50min = _early50min
        self.earlyMax = _earlyMax

        self.totalBasicSalary = _totalBasicSalary
        self.totalTransportation = _totalTransportation
        self.totalMedical = _totalMedical
        self.totalInjury = _totalInjury
        self.totalLunch = _totalLunch
        self.totalPosition = _totalPosition
        self.totalAddLunch = _totalAddLunch
        self.totalAddTransportation = _totalAddTransportation

        self.totalSundayWorked = _totalSundayWorked
        self.totalSundayHours = _totalSundayHours

        self.totalHolidayWorked = _totalHolidayWorked
        self.totalHolidayHours = _totalHolidayHours

        self.late5birr = _late5birr
        self.late10birr = _late10birr
        self.late20birr =_late20birr
        self.late50birr = _late50birr
        self.lateMaxBirr = _lateMaxbirr

        self.early5birr = _early5birr
        self.early10birr = _early10birr
        self.early20birr = _early20birr
        self.early50birr = _early50birr
        self.earlyMaxbirr = _earlyMaxbirr
        
        self.totalOTnormal = _totalOTnormal
        self.totalHolidayPay = _totalHolidayPay
        self.totalSundayPay = _totalSundayPay


    # Getter functions
    def getId(self):
        return self.id
        
    def getName(self):
        return self.name

    def getDaysWorked(self):
        return self.daysWorked
    
    def getOTworked(self):
        return self.OTworked

    def getAddAllow(self):
        return self.addAllowance
    
    def getSubTotal(self):
        return self.subtotal
    
    def getSubTotalWithAdd(self):
        return self.STwithAddAllow
    
    def getDeductions(self):
        return self.deductions

    def getIncomeTax(self):
        return self.incomeTax

    def getPension(self):
        return self.pension
    
    def getTotalDeductions(self):
        return self.totalDeductions

    def getTotalBeforeBonus(self):
        return self.totalBeforeBonus
    
    def getFullAttend(self):
        return self.fullAttend
    
    def getDiplomaBonus(self):
        return self.diplomaBonus
    
    def getLeadershipBonus(self):
        return self.leadershipBonus
    
    def getServiceBonus(self):
        return self.serviceBonus
    
    def getGrandTotal(self):
        return self.grandTotal
    
    def getLate5Min(self):
        return self.late5min

    def getLate10Min(self):
        return self.late10min
    
    def getLate20Min(self):
        return self.late20min

    def getLate50Min(self):
        return self.late50min

    def getLateMax(self):
        return self.lateMax

    def getEarly5Min(self):
        return self.early5min

    def getEarly10Min(self):
        return self.early10min
    
    def getEarly20Min(self):
        return self.early20min

    def getEarly50Min(self):
        return self.early50min

    def getEarlyMax(self):
        return self.earlyMax

    def getTotalBasicSalary(self):
        return self.totalBasicSalary
    
    def getTotalTransportation(self):
        return self.totalTransportation

    def getTotalMedical(self):
        return self.totalMedical 

    def getTotalInjury(self):
        return self.totalInjury

    def getTotalLunch(self):
        return self.totalLunch

    def getTotalPosition(self):
        return self.totalPosition

    def getTotalAddLunch(self):
        return self.totalAddLunch 

    def getTotalAddTransportation(self):
        return self.totalAddTransportation

    def getTotalSundayWorked(self):
        return self.totalSundayWorked

    def getTotalSundayHours(self):
        return self.totalSundayHours

    def getTotalHolidayWorked(self):
        return self.totalHolidayWorked

    def getTotalHolidayHours(self):
        return self.totalHolidayHours

    def getLate5birr(self):
        return self.late5birr

    def getLate10birr(self):
        return self.late10birr
    
    def getLate20birr(self):
        return self.late20birr

    def getLate50birr(self):
        return self.late50birr

    def getLateMaxbirr(self):
        return self.lateMaxBirr

    def getEarly5birr(self):
        return self.early5birr
    
    def getEarly10birr(self):
        return self.early10birr
    
    def getEarly20birr(self):
        return self.early20birr
    
    def getEarly50birr(self):
        return self.early50birr

    def getEarlyMaxbirr(self):
        return self.earlyMaxbirr

    def getTotalOTnormal(self):
        return self.totalOTnormal

    def getTotalHolidayPay(self):
        return self.totalHolidayPay

    def getTotalSundayPay(self):
        return self.totalSundayPay
