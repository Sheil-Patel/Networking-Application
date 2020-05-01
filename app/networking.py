#Networking-Application/networking.py

#TODO:

import os
from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_first_name():
    while True:
        first_name = input("Please input your first name\n")
        if first_name == "":
            print("Please input a first name please")
        else:
            break
    return first_name
def get_last_name():
    last_name = input("Please input your last name\n")
    while True:
        if last_name == "":
            print("Please input a last name please")
        else:
            break
    return last_name
def get_email():
    email = input("Please input email in form 'example@gmail.com'\n")
    return email
def get_phone_number():
    phone_number = input("Please input your phone number(no dashes please)\n")
    return phone_number
def create_contact(first_name, last_name, email, phone_number):
    dictionary = {"first_name": first_name , 
    "last_name" : last_name , "email" : email , "phone_number" : phone_number}
    return dictionary
def reading_from_sheet(doc,rows):
    #
    # READ SHEET VALUES
    #

    print("-----------------")
    print("SPREADSHEET:", doc.title)
    print("-----------------")

    for row in rows:
        print(row) #> <class 'dict'>
def writing_to_sheet(info,sheet,rows):
    next_id = len(rows) + 1 # TODO: should change this to be one greater than the current maximum id value
    
    next_row = list(info.values())#> [13, 'Product 13', 'snacks', 4.99, '2019-01-01']

    next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

    response = sheet.insert_row(next_row, next_row_number)

    print("-----------------")
    print("NEW RECORD:")
    print(next_row)
    print("-----------------")
    print("RESPONSE:")
    print(type(response)) #> dict
    print(response) #> {'spreadsheetId': '___', 'updatedRange': '___', 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}

if __name__ == "__main__":
    
    first_name = get_first_name()
    last_name = get_last_name()
    email = get_email()
    phone_number = get_phone_number()
    contact = create_contact(first_name, last_name, email, phone_number)
    
    networking_contacts = []
    networking_contacts.append(contact) # Appends contact to list (dictionary to list)
    #print(networking_contacts[0]["phone_number"]) # should print phone number
    
    info = networking_contacts[0]

    load_dotenv()

    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
    SHEET_NAME = os.environ.get("SHEET_NAME", "Products")
    #
    # AUTHORIZATION
    #

    CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "google_api_credentials.json")

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

    
    #
    #Sheets stuff
    #
    client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
    doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
    sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
    rows = sheet.get_all_records() #> <class 'list'>
    #
    # READ VALUES FROM SHEET
    #
    reading_from_sheet(doc, rows)
    #
    # WRITE VALUES TO SHEET
    #
    writing_to_sheet(info,sheet,rows)
   

   

