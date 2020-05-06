# Azoff Networking Application
Welcome, say hello to our virtual networking assistant Azoff. After following the instruction below, you should be able to network more effectively using Azoff. Once you start Azoff, you will be prompted to input some information about yourself so we can tailor the program to you. After that you can navigate our menu and activate many of Azoff's functionalities listed below. Addtionally, Azoff uses a google sheet data store, which stores all your contacts - more information on this is stated below

## Menu Options

1. Input New Contacts Information
2. Read your libraray of Contacts
3. Receive tailored networking suggestions
4. Update your personal contact information

### External Google Sheet Datastore

Azoff stores your contact information on a google sheet that is only accessible to you. On that sheet, you will be able to see all the information on your inputted contacts such as their company, name, email, phone number, where and when you ment, and any other additional notes. Additionally, it will store the date you last contacted them and will send you optional push notifications if you have not been in contact with a person in your network for 15 days. This latter part is done by using the "Heroku Scheduler" application, which will be explained below. 


## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Setup

### Repo-Setup
Use the GitHub.com online interface to create a new remote project repository called something like "Azoff". When prompted by the GitHub.com online interface, let's get in the habit of adding a "README.md" file and a Python-flavored ".gitignore" file (and also optionally a "LICENSE") during the repo creation process. After this process is complete, you should be able to view the repo on GitHub.com at an address like `https://github.com/YOUR_USERNAME/Azoff`.

After creating the remote repo, use GitHub Desktop software or the command-line to fork this repo. Then, download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line:

```sh
cd ~/Desktop/Azoff
```
### Environment Setup
Use Anaconda to create and activate a new virtual environment, perhaps called "Azoff-env":

```sh
conda create -n Azoff-env python=3.7 # (first time only)
conda activate Azoff-env
```
### Installation of Packages
From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

### API key setup

## Sendgrid API
Your program will need an API Key to issue requests to the Sendgrid API. This will allow you to send emails to yourself.

Create a .env file located in cd ~/Desktop/robo-advisor and insert your own API key like the example below

```sh
SENDGRID_API_KEY="abc123"
```
Additionally, you will need to specify your own email address
```sh
MY_EMAIL_ADDRESS="abc123@gmail.com"
```
## Google Drive & Sheets API
In order to get access to a google sheet with your contact's information, you will need to set up the google drive and sheets API. Instructions for that can be found at this link. Dont forget to create an "auth" folder in the root folder of your directory!

```sh
https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/gspread.md
```

Once you have completed those instructions and successfully linked your project to a google sheet, you will need to add the Google Sheet ID into the environment variables. You can find this by looking at the URL of your Google Sheet. If the URL of your Google Sheet looks like this...
```sh
https://docs.google.com/spreadsheets/d/1RieDnIbsiAxJRcgQ9ZBjtULkyZDbJJ887l_vAkk_GQl/edit#gid=0
```

...you would need to insert the environment variable like below

```sh
GOOGLE_SHEET_ID = 1RieDnIbsiAxJRcgQ9ZBjtULkyZDbJJ887l_vAkk_GQl
```
Next you will need to create title the first sheet "Data" and add another sheet titled "Personal Information" . FYI, the sheets can be named whatever you want, just as long as what you name them matches the environment variable you input. 

```sh
SHEET_NAME = Data
SHEET_NAME2 = Personal Info
```

## LinkedIn Scraping Instructions
Azoff lets you scrape linkedIn in order to help you find people at the same firm as your contact book! 

In order to set this up you will need to install chromedriver onto your computer. 

Instructions for how to install can be found here: https://chromedriver.chromium.org/

Once you have downloaded the file, place it somewhere for later use such as your desktop. 

Once you have relocated it, copy the path name and within the `def link(contactINFO):` function place the path name below. 

```sh
driver = webdriver.Chrome('ENTER_PATH_NAME_HERE')
```

## Running the program

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/networking.py
```
This command should allow you to access our menu and select the following options via a menu:

1. Input New Contacts Information
2. Read your libraray of Contacts
3. Receive tailored networking suggestions
4. Update your personal contact information


## Heroku Capability Instructions
In order to use implement our automatic push notification system, you will need to setup a Heroku account and use "Heroku Scheduler." Instructions on how to do this can be found at this link below
```sh
https://github.com/prof-rossetti/intro-to-python/blob/master/notes/clis/heroku.md
```
Once you have created an application on Heroku, you must do the following steps. If are having trouble, reference the link above:

1. Remove the following line from the .gitignore file from your root directory
```sh
auth/google_api_credentials.json
```
2. Push your code to Heroku using
```sh
git push heroku master
```
3. When you are in your application on the Heroku website,go to the "settings" tab and add all your environment variables from your .env folder
4. Go to "Applications" and enable the Heroku Scheduler to run the code below once daily

```sh
python app/automation.py
```
This code will send you a push notification if you have not reached out to a contact after 15 days.


## Testing Capabilities

### Testing with Pytest Package
After installing your package dependencies through requirments.txt, you are able to use the "pytest" package. By entering the command below, you are able to run the tests inputted in the file located at Test/my_test.py

```sh
pytest
```

### Automatic Testing with Travis-CI and Code Climate

Travis-CI: Code is compatible with Travis-CI to run tests to see if fundamental program functions are working properly.

Code Climate: Code can be used with Code Climate to check coding syntax and style
