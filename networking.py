#Networking-Application/networking.py

#TODO:

import os

def get_first_name():
    while True:
        first_name = input("Please input your first name\n")
        if first_name == "":
            print("Please input a first name please")
        else:
            break
    return first_name
def get_last_name():
    last_name = input("Please input your first name\n")
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
    
if __name__ == "__main__":
    
    first_name = get_first_name()
    last_name = get_last_name()
    email = get_email()
    phone_number = get_phone_number()
    contact = create_contact(first_name, last_name, email, phone_number)
    
    networking_contacts = []
    networking_contacts.append(contact) # Appends contact to list (dictionary to list)
    print(networking_contacts[0]["phone_number"]) # should print phone number
    
    
