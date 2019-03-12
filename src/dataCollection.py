#Developed by Trey Walker for The Butterknife   
from __future__ import print_function #Google
from apiclient import discovery #Google API
from oauth2client import client #Google API
from oauth2client import tools #Google API
from oauth2client.file import Storage #Google API
import httplib2 #For HTTP Usage
import requests #For HTTP Usage
import os #For Local File Usage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'src\client_secret.json' #Goto Google's API Dev
APPLICATION_NAME = '2019 Scout Form' #Name of Application

def get_credentials():
    #Gets the credentials to run the Google API
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
 
def getSheet(range):
    print("Collecting "+range+"... ", end="", flush=True)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1ZHUgT7rR1FEvwyHb5Emm8U5qYWNtRTGN3VrJJQ74txk' #Google Sheet ID
    rangeName = range #Range
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('FAILED!')
        return(False)
    else:
        print('DONE!')
        return(values)


if __name__ == '__main__':
    print(getSheet('B2:P'))
