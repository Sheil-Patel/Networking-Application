import os
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta 
#Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials



if __name__ == "__main__":
  #Authorization
  CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "google_api_credentials.json")

  AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

  credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
    
  load_dotenv()

  DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
  SHEET_NAME = os.environ.get("SHEET_NAME", "Products")
  SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
  MY_EMAIL = os.environ.get("MY_EMAIL_ADDRESS")

  client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
  doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
  sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
  rows = sheet.get_all_records() #> <class 'list'>

  last_notification_info = []
  last_notification = sheet.col_values(11)
  remove = last_notification.pop(0) #removes header

  time_diff = timedelta(days = 15)
  today = datetime.today()
  
  date_last_contacted_info = []
  date_last_contacted = sheet.col_values(9)
  remove = date_last_contacted.pop(0) #removes header


  #date_obj_ex = datetime.strptime("05/02/20", "%m/%d/%y")
  
  x = 1
  for dates in last_notification:
      date_obj = datetime.strptime(dates,"%m/%d/%y")
      cell = {"column" : 11 , "row" : x , "value" : date_obj}
      last_notification_info.append(cell)
      x+=1

  
  for contacts in last_notification_info:
    last_push_date = contacts["value"]
    threshold_date = time_diff + last_push_date
    if threshold_date == today: # Fires when 15 days past the last pushed date is equivalent to today's date
      row_num = contacts["row"]
      
      sheet.update_cell(10, row_num, date_last_contacted[row_num]) # Updates Date of Last Contacte -> Second most recent date of contact
      sheet.update_cell(9,row_num, threshold_date)# Updates Date of last pushed -> Date of Last Contacted



  #Access data
  # sheet.col_values(1)
  # sheet.cell(2,1).value

  # update cell
  # sheet.update_cell(3,1,"Bobcats")

  #Findining Specific object and returning position
  # cell_list = sheet.findall("Cats")
  # for cell in cell_list:
  #         print(cell.value)
  #         print(cell.row)
  #         print(cell.col)

  