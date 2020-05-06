import os
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta 
#Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *
#From Networking
from networking import suggestions_func, get_yourContactINFO
#Sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from gspread_formatting import *
from pprint import pprint


format_highlight = cellFormat(
    backgroundColor = color(10, 10, 200),
    textFormat =textFormat(bold=False) , 
    horizontalAlignment = 'RIGHT'
)
def send_email(subject, html, yourcontactINFO):
  """ 
  Sends email. Passes in subject, html, and contact information from spreadsheet 
  Important thing to note here is that the email is passed in via the google sheets and thus can be changed whenever
  """

  emailAddress = yourcontactINFO['Email']

  client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
  #print("CLIENT:", type(client))
  #print("SUBJECT:", subject)
  #print("HTML:", html)
  message = Mail(from_email=MY_EMAIL, to_emails=emailAddress, subject=subject, html_content=html)
  try:
      response = client.send(message)
      #print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
      #print(response.status_code) #> 202 indicates SUCCESS
      if response.status_code == 202:
          print(f"An email with Suggestions has been sent to { yourcontactINFO['Email'] }")
      else:
          print("Oops! An Error Occured While Trying to Send Email!")
          print("Please Ensure That You Have Entered a Correctly Formatted Email in Your Spreadsheet!")

      return response
  except Exception as e:
      print("OOPS", e.message)
      return None

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
  SHEET_NAME2 = os.environ.get("SHEET_NAME2", "Personal Info")
  SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
  MY_EMAIL = os.environ.get("MY_EMAIL_ADDRESS")

  client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
  doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
  sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
  rows = sheet.get_all_records() #> <class 'list'>


  sheet2 = doc.worksheet(SHEET_NAME2)
  rows2 = sheet2.get_all_records()
  
  last_notification_info = []
  last_notification = sheet.col_values(11)
  remove = last_notification.pop(0) #removes header

  time_diff = timedelta(days = 15)
  today = datetime.today()
  date_str = datetime.strftime(today,"%m/%d/%y")
  

  date_last_contacted = sheet.col_values(9)
  remove = date_last_contacted.pop(0) #removes header
  yourcontactINFO = get_yourContactINFO(rows2)
  opportunities = ""
  


  
  #date_obj_ex = datetime.strptime("05/02/20", "%m/%d/%y")

  x = 2
  for dates in last_notification:
      date_obj = datetime.strptime(dates,"%m/%d/%y")
      threshold_date = time_diff + date_obj
      threshold_date_str = datetime.strftime(threshold_date,"%m/%d/%y")
      cell = {"column" : 11 , "row" : x , "datetime" : date_obj, "string": dates, "threshold": threshold_date_str}
      last_notification_info.append(cell)
      x+=1
  
  
  for contacts in last_notification_info:
    threshold = contacts["threshold"]
    if threshold == date_str: # Fires when 15 days past the last pushed date is equivalent to today's date
      row_num = contacts["row"]
      plug = date_last_contacted[row_num-2]
      sheet.update_cell(row_num, 10, plug ) # Updates Date of Last Contact -> Second most recent date of contact
      sheet.update_cell(row_num, 9, date_str)# Updates Date of last push notifaction(Current Date)-> Date of Last Contacted
      sheet.update_cell(row_num, 11, date_str) # Updates date of last push notification --> Current Date
      Location = 'I' + str(row_num)
      format_cell_range(sheet, Location , format_highlight)
      contactINFO = rows[row_num-2]
      suggestions = suggestions_func(contactINFO, yourcontactINFO, opportunities)
      subject = (f"[Modern Dealbook] Automated Requested Suggestion for {contactINFO['First Name']} {contactINFO['Last Name']} ")

      html = f"""
        <img src="https://i0.wp.com/arielle.com.au/wp-content/uploads/2016/04/urban-nyc-light.jpg"> 

        <h3> Hi, {yourcontactINFO['Your First Name']}! </h3>
        <h4> We noticed its been a while since you talked to {contactINFO['First Name']} {contactINFO['Last Name']} at {contactINFO['Company']} </h4>
        <h4> We compiled a suggested email for you to send to {contactINFO['First Name']} to touch base and keep the relationship alive! </h4>  

        {suggestions[3]['Template']}
        <h4> Feel Free to Copy and Paste this Draft to send to {contactINFO['First Name']} at {contactINFO['Email']} </h4>  

        <h4> Dont Forget To Proof Read!</h4>  

        """
      send_email(subject,html,yourcontactINFO)
    
