# Salary Calculator

## Overview
Salary Calculator is an app created to automate the salary calculation process by retrieving each employees attendance data and 
salary sheet from googlespreadsheets with the help of google's API. This App is built specifically to meet the demands and requirements of 
a particular company. This code will only work with the data provided from the company. However, the code can easily modified to be 
compatible with other spreadsheet that are formatted differently.
<br/><br/>
**You will not be able to retrieve any data without the secret key.**

![preview](https://user-images.githubusercontent.com/22732115/194951710-cca57a0f-053f-4f0f-b7e5-177976399d47.png)

## Important
To pull data from the spreadsheet, it has to be shared with the following service account: <br/>
accessgoogleapis@salarycalculator-364616.iam.gserviceaccount.com

- new link -
dataretrieveraccount@salarycalculator-382414.iam.gserviceaccount.com

To build the .exe run "pyinstaller -f app.py"

## Library used
  * gspread - To Fetch spreadsheet data  
  * Pandas - To create and organize the dataframe
  * Tkinter - To display the App
  * PyInstaller - To create an executable
  
## Built with           
<code><img height="20" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" /></code>

          
