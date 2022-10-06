from data.employeeData import employeeData
from data.processData import processData

attendance = employeeData()
attendance = attendance.getSpreadSheet("https://docs.google.com/spreadsheets/d/1pPt4M50dhPWkGLJKGGBO-msXP4grRbQvk8n_CTx0qBQ/edit#gid=429097067")
attendance = attendance.worksheet("考勤记录")

process = processData(attendance)

exception = [{"date":10, "exception":"dayOff"}, {"date":12,"exception":"dayOff"}, {"date":13,"exception":"dayOff"}]
# note-to-self if not empty append, else create the array
exception.extend([{"date":27, "exception":"dayOff"}, {"date":28, "exception":"dayOff"}])
exception.extend([{"date":26, "exception":"hourly"}, {"date":29, "exception":"hourly"}, {"date":30, "exception":"hourly"}])

process.calculateAttendance(exception)