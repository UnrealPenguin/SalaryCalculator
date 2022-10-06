import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

cred = ServiceAccountCredentials.from_json_keyfile_name("data\secret_key.json", scopes=scopes)

file = gspread.authorize(cred)

sh = file.open_by_url("https://docs.google.com/spreadsheets/d/1pPt4M50dhPWkGLJKGGBO-msXP4grRbQvk8n_CTx0qBQ/edit#gid=429097067")
# sheet = sh.sheet1

# print(sheet.acell('A2').value)