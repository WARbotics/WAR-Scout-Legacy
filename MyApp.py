from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import tbapy
import httplib2
import os
import requests
import numpy
import pandas as pd
import matplotlib
from datetime import date
import texttable as tt

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'WARScout'
key = "6ZS9aeVtUuidbC2byVYnLlAuIid60ipTXZbuWkGLffCTEY5nrMjdiV6EUUQTodmK"
tba = tbapy.TBA(key)
event = "2018gagr"

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """
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
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getSheet():
    global list
    list = []
    x = 0

    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1C8Jgf7W5VTzNBMeYhkVsjFx3g6fqF8MzqdUfIvHAMDE'
    rangeName = 'B2:K'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    #for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
    #    print('%s, %s' % (row[0], row[4]))
    for row in values:
        while x < 10:
            list.append(str(row[x]))
            x = x + 1

def status():
    #figuring out if TBA is actually online
    statusCheck = tba.status()
    if statusCheck['is_datafeed_down'] == False:
        pass
    else:
        print ('Team Blue alliance systems are down')
        exit()

#def __init__():
#    get_credentials()
#    getSheet()
#    print(str(list[0]))
    # print("WAR botics FRC scouting script")
def getTeamNumber():
    teamNumber = list[0]
def getAutoCrossLine(auto):
    auto = list[2]
    return auto
def getTeamData():
    #collecting data
    getTeamNumber()
    mainTeam = tba.team(teamNumber, False)
    nickName = mainTeam['nickname']
    teamWebsite = mainTeam['website']
    rookieYear = mainTeam['rookie_year']
#def teamAge(rookieYear, Age):
    #clean this mess

    #year = date.today().year
    #rookieYear - year = Age
    #return Age
#def dataAnalysis(Age):
    #pass
#def leaderboard():
    #teamAge()
    #getTeamNumber()
    #getTeamData()
    #lb = pd.DataFrame({'Team name':  [nickName], 'Team Number': [teamNumber], 'Ranking score' []})
    #^^^ write the leaderboard score system
    #lb = lb.sort(['Team name', 'Team Number', 'Ranking score'], ascending=[1,0])
    #print (lb)


if __name__ == '__main__':
    get_credentials()
    getSheet()
    print (getTeamNumber())
