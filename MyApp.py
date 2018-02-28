#Devloped by Victor H. and Trey W.
#Team 6925
from __future__ import print_function #Google API Stuff
from apiclient import discovery #Google API Stuff
from oauth2client import client #Google API Stuff
from oauth2client import tools #Google API Stuff
from oauth2client.file import Storage #Google API Stuff
import tbapy
import httplib2
import os
import requests
import numpy
import pandas as pd
import matplotlib
from datetime import datetime #Gets Date
import texttable as tt

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json' #Goto Google's API Dev
APPLICATION_NAME = 'WARScout'
key = "6ZS9aeVtUuidbC2byVYnLlAuIid60ipTXZbuWkGLffCTEY5nrMjdiV6EUUQTodmK" #TBA Key
tba = tbapy.TBA(key)
year = datetime.now().year #Gets Year
lastyear = year - 1
event = str(year) + 'gagr'
lastevent = (str(lastyear))+ 'gagr'
x = 0 #Do not change
infinite = 0 #No not change

def get_credentials():

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

def getSheet(): #Scrapes information off of the quanatiative
    global list
    list = []

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1C8Jgf7W5VTzNBMeYhkVsjFx3g6fqF8MzqdUfIvHAMDE' #Google Sheet ID
    rangeName = 'B2:K' #Range
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

def findInfo(sendy, y): #Makes the List
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

def getList(get): #Gathers Information to make a list
    newList = []
    newList.append(findInfo(newList, get))
    del newList[len(newList)-1]
    return(newList)
def getTeamNumber():
    teamList = []
    teamList.append(findInfo(teamList, 0))
    del teamList[len(teamList)-1]
    return(teamList)

def teamDictMaker(): #Puts all the Team Information into a dictionary
    x = 0
    global teamDict
    teamDict = {}
    getSheet() #Updates Information
    for infinite in range(0, 1000):
        try:
            add = {(getTeamNumber()[x]):[(getList(1)[x]), (getList(2)[x]),
                                         (getList(3)[x]), (getList(4)[x]),
                                         (getList(5)[x]), (getList(6)[x]),
            (getList(7)[x]), (getList(8)[x]), (getList(9)[x]), (getTeamData(getTeamNumber()[x]))]}
            teamDict.update(add)
            x = x + 1
        except:
            return(teamDict)

def get2017Data(teamBlankNumber):
    eventdata = tba.event_teams(lastevent, True, True)
    teamsAtEvent = len(eventdata)
    ranking = tba.event_rankings(lastevent)
    y = '1'
    teamFRCNumber = 'frc' + str(teamBlankNumber)
    for y in range(1, teamsAtEvent):
        frc_team = ranking['rankings'][y]['team_key']
        if frc_team == teamFRCNumber:
            print (y)
            #collects all of last years data for team that is needed
            frc_team = ranking['rankings'][y]
            getDQ = ranking['rankings'][y]['dq']
            getRank = ranking['rankings'][y]['rank']
            getRecord = ranking['rankings'][y]['record']
            getWins = ranking['rankings'][y]['record']['wins']
            getLoses = ranking['rankings'][y]['record']['losses']
            getTies = ranking['rankings'][y]['record']['ties']
            getPlay = ranking['rankings'][y]['matches_played']
            teamPastDictGet = {'Frc team': frc_team, 'DQ': getDQ, 'Ranking': getRank,
                               'Record': getRecord,'Wins': getWins, 'Loses': getLoses,
                               'Ties': getTies, 'Matches Played': getPlay}
            return teamPastDictGet
def getTeamData(teamNumber):
    #collecting data
    mainTeam = tba.team(teamNumber, False)
    nickName = mainTeam['nickname']
    teamWebsite = mainTeam['website']
    rookieYear = mainTeam['rookie_year']
    teamdata = {'Nick name': nickName, 'Team website': teamWebsite, 'rookie year': rookieYear}
    return teamdata
def teamAge(rookieY):
    #clean this mess
    year = date.today().year
    Age = rookieY - year
    return Age
def dataAnalysis(age, rank, wins, DQ, loses):
    g_score = age + getRank + getWins
    b_score = getDQ + getLoses
    score = g_score - b_score
    return score
    #^^ this just basic for testing
if __name__ == '__main__':
    get_credentials()
    teamDictMaker()
    print (get2017Data(6325))
    print (getTeamData(6325))
    print (teamAge(getTeamData(teamdata['rookie year']))
