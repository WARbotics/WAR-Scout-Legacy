
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
lastevent = "2017gagr"
x = 0

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
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getSheet():
    global list
    list = []

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
        for x in range(0, 10):
            list.append(str(row[x]))
            x = x + 1

def findInfo(sendy, y):
    while True:
        try:
            x = x + y
            sendy.append(list[x])
        except:
            return(sendy)

def status():
    #figuring out if TBA is actually online
    statusCheck = tba.status()
    if statusCheck['is_datafeed_down'] == False:
        pass
    else:
        print ('Team Blue alliance systems are down')
        exit()
def getTeamNumber():
    teamList = [list[0]]
    teamList = findInfo(teamList, 10)
    for teamList
    return(teamList)

def listSplitter(sList, catch):
    newList = {}
    for sList in range(0, len(sList)):
        newList.update({catch + sList[x]})



def getAutoCrossLine(teamNumber):
    autolist = [list[2]]
    autoList = findInfo(autoList, 11)
    return(autoList)
def setTeamName(teamNumber):
    teamNumber getTeamNumber()
def get2017Data():
    ranking = tba.event_rankings(lastevent)
    team = setTeamName()
    #added the value of teamNumber ^^^^
    y = '1'
    for y in range(1, 40):
        frc_team = ranking['rankings'][y]['team_key']
        if frc_team == team:
            return(frc_team)


def getTeamData(teamNumber):
    #collecting data

    getTeamNumber()
    mainTeam = tba.team(teamNumber, False)
    nickName = mainTeam['nickname']
    teamWebsite = mainTeam['website']
    rookieYear = mainTeam['rookie_year']
    teamdata = {'Nick name': nickName, 'Team website': teamWebsite, 'rookie year': rookieYear}
    return teamdata
def teamAge(Age):
    #clean this mess
    t = getTeamData()
    rookieY = t.teamdata['rookie year']
    year = date.today().year
    Age = rookieY - year
    return Age
def dataAnalysis(self):
    self.teamAge(0)
    number = self.getTeamNumber()
    self.getTeamData(number)

def leaderboard(self):
    self.teamAge(0)
    getTeamNumber()
    getTeamData()
    df = df.DataFrame({'Team name':  [nickName], 'Team Number': [teamNumber]})
    #^^^ write the leaderboard score system. ADD the Score
    df = df.sort(['Team name', 'Team Number', 'Ranking score'], ascending=[1,0])
    print (df)


if __name__ == '__main__':
    get_credentials()
    getSheet()
    t = getTeamNumber()
    print (t)
