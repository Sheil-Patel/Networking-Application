from app.networking import link, print_headers, print_personal_headers, create_contact, reading_from_sheet, writing_to_sheet, get_suggestion, send_email, display_templates, get_yourContactINFO
import os, pytest, gspread
#Sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from gspread_formatting import *
from pprint import pprint



def test_create_contact():
    dictionary = {"company":"Microsoft","first_name": "Bill" , 
    "last_name" : "Gates" , "email" :"bill.gates@microsoft.com" , "phone_number" : "2467899082", "where_we_met": "At Microsoft", 
    "notes": "His wife is Melinda", "date_added": "03/15/20", "date_last_contacted" : "03/15/20", "second_most_recent_date": "", 
    "date_of_last_notification" : "03/15/20"}
    assert create_contact("Microsoft", "Bill", "Gates" , "bill.gates@microsoft.com", "2467899082", "At Microsoft", "His wife is Melinda", "03/15/20",  "03/15/20" , "" , "03/15/20") == dictionary
    #Tests if the create contact code correctly parses information into a dictionary

#def test_send_email():
#    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
#    MY_EMAIL = os.environ.get("MY_EMAIL_ADDRESS")
#    subject = "Hello"
#    html = f"""  This is an example email """
#    yourcontactINFO = [{"Your First Name":"Bill", "Your Last Name": "Gates", "Email": "bill.gates@microsoft.com", "Your Current University": "N/A", "Your Majors": "Computer Science", "Your Class Year": "Class of 1978"}]
#    assert send_email(subject,html, yourcontactINFO) == 202

def test_get_yourContactINFO():
    rows2 = [{"Your First Name":"Bill", "Your Last Name": "Gates", "Email": "bill.gates@microsoft.com", "Your Current University": "N/A", "Your Majors": "Computer Science", "Your Class Year": "Class of 1978"}]
    
    dictionary = {"Your First Name":"Bill", "Your Last Name": "Gates", "Email": "bill.gates@microsoft.com", "Your Current University": "N/A", "Your Majors": "Computer Science", "Your Class Year": "Class of 1978"}
    get_yourContactINFO(rows2) == dictionary


    