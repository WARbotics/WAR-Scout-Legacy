#Devloped by Victor H. and Trey W.
#Team 6925
from __future__ import print_function #Google API Stuff
from apiclient import discovery #Google API Stuff
from oauth2client import client #Google API Stuff
from oauth2client import tools #Google API Stuff
from oauth2client.file import Storage #Google API Stuff
import tbapy #The blue alliance API
import httplib2
import os
import requests
from datetime import datetime #Gets Date
# DATA
import pandas as pd
import numpy as np

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
    global mainList
    mainList = []

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
    for row in values:
        for x in range(0, 9):
            mainList.append(str(row[x]))
            x = x + 1

def findInfo(sendy, y): #Makes the List
    x = y
    for infinite in range(0, 1000):
        try:
            sendy.append(mainList[x])
            x = x + 9
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
def getTeamNumber(): #Makes a list of teams scouted
    teamList = []
    teamList.append(findInfo(teamList, 0))
    del teamList[len(teamList)-1]
    return(teamList)

def getScoutingData():
    scoutingData = {}
    scoutingDataList = []
    x = 0
    for x in range(0, len(getTeamNumber())):
        add = {'Auto Actions':(getList(1)[x]),
        'teleopHighGoals':(getList(2)[x]),
        'teleopLowGoals':(getList(3)[x]),
        'vaults':(getList(4)[x]),
        'usefull':(getList(5)[x]),
        'rating':(getList(6)[x]),
        'climb':(getList(7)[x]),
        'response':(getList(8)[x])}
        scoutingData.update(add)
        scoutingDataList.append(scoutingData)
        scoutingData = {}
    x = 0
    #for x in range(0, (len(getTeamNumber()))):
    return(scoutingDataList)

def perCal(y):
    per = y/len(getTeamNumber())
    per = per * 100
    round(per,0)
    per = int(per)
    per = (str(per)+'%')
    return(per)


def teamDictMaker():
    scoutingData = getScoutingData()
    #Puts all the T.eam Information into a dictionary
    x = 0
    global teamDict
    teamDict = {}
    teamList = getTeamNumber()
    checked = []
    getSheet()
    #Updates Information
    for x in range(0, len(teamList)):
        if teamList[x] in checked:
            checked.append(teamList[x])
            add2 = scoutingData[x]
            add1 = teamDict[teamList[x]]
            climbList = []
            autoActionList = []
            climbList.append(add1['climb'])
            climbList.append(add2['climb'])
            autoActionList.append(add1['Auto Actions'])
            autoActionList.append(add2['Auto Actions'])
            add3 = {
            'Auto Actions':autoActionList,
            'teleopHighGoals':(str(int((add1['teleopHighGoals']))+(int(add2['teleopHighGoals'])))),
            'teleopLowGoals':(str(int((add1['teleopLowGoals']))+(int(add2['teleopLowGoals'])))),
            'vaults':(str(int((add1['vaults']))+(int(add2['vaults'])))),
            'usefull':(str(int((add1['usefull']))+(int(add2['usefull'])))),
            'rating':(str(int((add1['rating']))+(int(add2['rating'])))),
            'climb':climbList,
            'response':((add1['response'])+'; '+(add2['response'])),
            'matchesRec':(str(int(checked.count(teamList[x]))))}
            add = {teamList[x]: (add3)}
        else:
            checked.append(teamList[x])
            y = scoutingData[x]
            add2 = {
            'Auto Actions':(y['Auto Actions']),
            'teleopHighGoals':(y['teleopHighGoals']),
            'teleopLowGoals':(y['teleopLowGoals']),
            'vaults':(y['vaults']),
            'usefull':(y['usefull']),
            'rating':(y['rating']),
            'climb':(y['climb']),
            'response':(y['response']),
            'matchesRec':(1)}
            add = {(teamList[x]): (add2)}
        teamDict.update(add)
    return(teamDict)


def getHistoricData(teamBlankNumber):
    eventdata = tba.event_teams(lastevent, True, True)
    teamsAtEvent = len(eventdata)
    ranking = tba.event_rankings(lastevent)
    teamFRCNumber = 'frc' + str(teamBlankNumber)
    for y in range(1, teamsAtEvent):
        frc_team = ranking['rankings'][y]['team_key']
        if frc_team == teamFRCNumber:
            #collects all of last years data for team that is needed
            frc_team = ranking['rankings'][y]
            getDQ = ranking['rankings'][y]['dq']
            getRank = ranking['rankings'][y]['rank']
            getWins = ranking['rankings'][y]['record']['wins']
            getLoses = ranking['rankings'][y]['record']['losses']
            getWinLoseRat = int(getWins)/int(getLoses)
            getPlay = ranking['rankings'][y]['matches_played']
            teamPastDictGet = {'Frc team': frc_team, 'DQ': getDQ, 'Ranking': getRank, 'Win Loss Ratio': str(getWinLoseRat),
                               'Matches Played': getPlay}
            return teamPastDictGet
    teamPastDictGet = {'Frc team': 'No HIS', 'DQ': 'No HIS', 'Ranking': 'No HIS',
    'Win Loss Ratio': 'No HIS', 'Matches Played': 'No HIS'}
    return teamPastDictGet

def getTeamData(teamNumber):
    #collecting data
    mainTeam = tba.team(teamNumber, False)
    nickName = mainTeam['nickname']
    teamWebsite = mainTeam['website']
    rookieYear = mainTeam['rookie_year']
    teamdata = {'Nick name': nickName, 'Team website': teamWebsite, 'rookie year': rookieYear}
    #broken
    return teamdata
def teamAge(rookieY):
    #clean this mess
    year = date.today().year
    Age = rookieY - year
    return Age
def weightHistory():
    weightHistoryList = []
    for x in range(0, len(getTeamNumber())):
        getDQ = teamDict[getTeamNumber()[x]]['DQs']
        if getDQ == 'No HIS':
            pass
        else:
            getDQ = int(getDQ)
            if getDQ >= 1:
                getDQ * -10
            else:
                getDQ = 0
        getWLRatio = teamDict[getTeamNumber()[x]]['Win/Loss Ratio']
        if getWLRatio == 'No HIS':
            pass
        else:
            getWLRatio = float(getWLRatio)
            round(getWLRatio,1)
            getWLRatio = getWLRatio * 5
        if getDQ == 'No HIS':
            weightHistoryList.append('No HIS')
        else:
            history = getDQ + getWLRatio
            weightHistoryList.append(history)
    return(weightHistoryList)

def whole(y):
    round(y,0)
    int(y)
    return(y)

def weightActive():
    weightActiveList = []
    typeList = []
    for x in range(0, len(getTeamNumber())):
        weightAutoActions = 0
        teamList = getTeamNumber()[x]
        matches = int(teamDict[teamList]['matchesRec'])
        getAutoActions = teamDict[teamList]['Auto Actions']
        getTeleopHighGoals = int(teamDict[teamList]['teleopHighGoals'])
        getTeleopLowGoals = int(teamDict[teamList]['teleopLowGoals'])
        getVaults = int(teamDict[teamList]['vaults'])
        getUsefull = int(teamDict[teamList]['usefull'])
        climbList = teamDict[teamList]['climb']
        getRating = int(teamDict[teamList]['rating'])
        autoLow = getAutoActions.count('Crossed A-Line, Placed Cube on Switch')
        autoHigh = getAutoActions.count('Crossed A-Line, Placed Cube on Scale')
        autoCross = getAutoActions.count('Crossed A-Line')

        #Auto Data weighting
        if autoCross >= 1 or autoLow >= 1 or autoHigh >= 1:
            if autoCross >= 1:
                autoCross = ((autoCross+autoLow+autoHigh)/(matches))
                if autoCross >= 0.75:
                    weightAutoActions = weightAutoActions + 3
            if autoLow >= 1:
                autoLow = autoLow / matches
                if autoLow >= 0.4:
                    weightAutoActions = weightAutoActions + 6
            if autoHigh >= 1:
                autoHigh = autoHigh / matches
                if autoHigh >= 0.15:
                    weightAutoActions = weightAutoActions + 9

        #Teleop data weighting
        if getTeleopHighGoals >= 1:
            getTeleopHighGoals / matches
            getTeleopHighGoals = whole(getTeleopHighGoals)
            getTeleopHighGoals * 6
        else:
            getTeleopHighGoals = 0
        if getTeleopLowGoals >= 1:
            getTeleopLowGoals / matches
            getTeleopLowGoals = whole(getTeleopLowGoals)
            getTeleopLowGoals * 4
        else:
            getTeleopLowGoals = 0
        if getVaults >= 1:
            getVaults / matches
            getVaults = whole(getVaults)
            getVaults * 2

        getUsefull = getUsefull / matches
        getUsefull = whole(getUsefull)
        getRating = getRating / matches
        getRating = whole(getRating)

        if climbList.count('Yes') >= 1:
            weightClimber = (((climbList.count('Yes'))*(7))/(matches))
        else:
            weightClimber = 0

        #Type of Robot
        if getTeleopHighGoals > getTeleopLowGoals:
            if getTeleopHighGoals > getVaults:
                type = 'High Goal Shooter'
        if getTeleopLowGoals > getTeleopHighGoals:
            if getTeleopLowGoals > getVaults:
                type = 'Low Goal Shooter'
        if getVaults > getTeleopHighGoals:
            if getVaults > getTeleopLowGoals:
                type = 'Vault Main'
        active = (
        int(weightAutoActions) +
        int(getRating) +
        int(getTeleopHighGoals) +
        int(getTeleopLowGoals) +
        int(getUsefull) +
        int(getVaults) +
        int(weightClimber))
        weightActiveList.append(active)
        typeList.append(type)
    return(weightActiveList, typeList)

def dataAnalysis():
    aData = weightActive()
    weights = aData[0]
    typeList = aData[1]
    x = 0
    score = 0
    scoreList = []
    for x in range(0, len(getTeamNumber())):
        score = int(weights[x])
        type = typeList[x]
        response = teamDict[getTeamNumber()[x]]['response']
        round(score,0)
        score = int(score)
        score = str(score)
        if int(score) <= 9:
            finalList = ('Score: '+score+'     Type: '+type)
        else:
            finalList = ('Score: '+score+'    Type: '+type)
        if type == 'High Goal Shooter':
            finalList = (finalList+'    Response: '+response)
        elif type == 'Low Goal Shooter':
            finalList = (finalList+'     Response: '+response)
        elif type == 'Vault Main':
            finalList = (finalList+'            Response: '+response)
        scoreList.append(finalList)
    return(scoreList)

def getLeaderboard():
    getLeaderboard = {}
    data = dataAnalysis()
    for x in range(0, len(getTeamNumber())):
        add = {(getTeamNumber()[x]): (data[x])}
        getLeaderboard.update(add)
    return(getLeaderboard)


def finalPrint():
    leaderboard = getLeaderboard()
    print()
    checked = []
    for x in range(0, len(getTeamNumber())):
        if getTeamNumber()[x] in checked:
            continue
        if int(getTeamNumber()[x]) > 999:
            print(getTeamNumber()[x] + '    ' + (leaderboard[getTeamNumber()[x]]))
            checked.append(getTeamNumber()[x])
        elif int(getTeamNumber()[x]) <= 999:
            print(getTeamNumber()[x] + '     ' + (leaderboard[getTeamNumber()[x]]))
            checked.append(getTeamNumber()[x])
        elif int(getTeamNumber()[x]) <= 9:
            print(getTeamNumber()[x] + '      ' + (leaderboard[getTeamNumber()[x]]))
            checked.append(getTeamNumber()[x])
        print()

if __name__ == '__main__':
    get_credentials()
    getSheet()
    teamDictMaker()
    finalPrint()
