import gspread
from oauth2client.service_account import ServiceAccountCredentials

# NOTICE
# XLS files has to be converted to Google spreadsheet for this script to work
# Do not simply drag and drop the excel file to drive. Import it instead.

class getGspread:
    def __init__(self):
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        cred = ServiceAccountCredentials.from_json_keyfile_name("data\secret_key.json", scopes=scopes)
        self.file = gspread.authorize(cred)

    # name of spreadsheet in google Sheets (Has to be shared to the Service Account)
    def getSpreadSheet(self, _url):
        return self.file.open_by_url(_url)