
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
infinite = 0

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
    x = y
    for infinite in range(0, 1000):
        try:
            sendy.append(list[x])
            x = x + 10
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
    teamList = []
    teamList.append(findInfo(teamList, 0))
    del teamList[len(teamList)-1]
    return(teamList)
def getAuto():
    autoList = []
    autoList.append(findInfo(autoList, 1))
    del autoList[len(autoList)-1]
    return(autoList)
def getAutoHigh():
    autoHighList = []
    autoHighList.append(findInfo(autoHighList, 2))
    del autoHighList[len(autoHighList)-1]
    return(autoHighList)
def getAutoLow():
    autoLowList = []
    autoLowList.append(findInfo(autoLowList, 3))
    del autoLowList[len(autoLowList)-1]
    return(autoLowList)
def getTeleopHigh():
    teleopHighList = []
    teleopHighList.append(findInfo(teleopHighList, 4))
    del teleopHighList[len(teleopHighList)-1]
    return(teleopHighList)
def getTeleopLow():
    teleopLowList = []
    teleopLowList.append(findInfo(teleopLowList, 5))
    del teleopLowList[len(teleopLowList)-1]
    return(teleopLowList)
def getUsefull():
    usefullList = []
    usefullList.append(findInfo(usefullList, 6))
    del usefullList[len(usefullList)-1]
    return(usefullList)
def getDriveScore():
    driveList = []
    driveList.append(findInfo(driveList, 7))
    del driveList[len(driveList)-1]
    return(driveList)
def getCanClimb():
    climbList = []
    climbList.append(findInfo(climbList, 8))
    del climbList[len(climbList)-1]
    return(climbList)
def getFouls():
    foulList = []
    foulList.append(findInfo(foulList, 9))
    del foulList[len(foulList)-1]
    return(foulList)
def teamDictMaker():
    x = 0
    global teamDict
    teamDict = {}
    for infinite in range(0, 1000):
        try:
            add = {(getTeamNumber()[x]):[(getAuto()[x]), (getAutoHigh()[x]),
                                         (getAutoLow()[x]), (getTeleopHigh()[x]),
                                         (getTeleopLow()[x]), (getUsefull()[x]),
            (getDriveScore()[x]), (getCanClimb()[x]), (getFouls()[x])]}
            teamDict.update(add)
            x = x + 1
        except:
            return(teamDict)

def get2017Data(self, teamBlankNumber):
    eventdata = self.tba.event_teams(lastevent, True, True)
    teamsAtEvent = len(eventdata)
    ranking = self.tba.event_rankings(lastevent)
    y = '1'
    teamFRCNumber = 'frc' + teamBlankNumber
    for y in range(1, teamsAtEvent):
        frc_team = self.ranking['rankings'][y]['team_key']
        if frc_team == teamFRCNumber:
            rankingPosition = y
            print (rankingPosition)
            break
    #collects all of last years data for team that is needed
    frc_team = self.ranking['rankings'][y]
    getDQ = self.ranking['rankings'][y]['dq']
    getRank = self.ranking['rankings'][y]['rank']
    getRecord = self.ranking['rankings'][y]['record']
    getWins = self.ranking['rankings'][y]['record']['wins']
    getLoses = self.ranking['rankings'][y]['record']['losses']
    getTies = self.ranking['rankings'][y]['record']['ties']
    getPlay = self.ranking['rankings'][y]['matches_played']

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
    self.teamAge()
    number = self.getTeamNumber()
    self.getTeamData(number)
    get2017Data(number)
    g_score = rookieYear + getRank + getWins
    b_score = getDQ + getLoses
    score = g_score - b_score
    #^^ this just basic for testing

def leaderboard(self):
    self.teamAge(0)
    teamnumber = getTeamNumber()
    getTeamData(teamnumber)
    dataAnalysis()
    df = df.DataFrame({'Team name':  [nickName], 'Team Number': [teamNumber], 'Score': [score]})
    #^^^ write the leaderboard score system. ADD the Score
    #df = df.sort(['Team name', 'Team Number', 'Ranking score'], ascending=[1,0])
    print (df)


if __name__ == '__main__':
    get_credentials()
    getSheet()
    t = teamDictMaker()
    print (t)
