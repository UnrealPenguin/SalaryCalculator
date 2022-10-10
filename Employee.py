class Employee:
    def __init__(   self, _name, _daysWorked, _overtimeWorked, _additionalAllowance, _subTotal, _STwithAddAllow, 
                    _deductions, _incomeTax, _pension, _totalDeductions, _totalBeforeBonus,
                    _fullAttend, _diplomaBonus, _leadershipBonus, _serviceBonus, _grandTotal):

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

    # Getter functions
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