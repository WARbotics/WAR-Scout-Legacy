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
import requests #Handels Http requests
from datetime import datetime #Gets Date
# DATA
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json' #Goto Google's API Dev
APPLICATION_NAME = 'WARScout' #Name of Application
tba = tbapy.TBA('6ZS9aeVtUuidbC2byVYnLlAuIid60ipTXZbuWkGLffCTEY5nrMjdiV6EUUQTodmK')
year = datetime.now().year #Gets Year
lastyear = year - 1
event = str(year) + 'gagr'
lastevent = (str(lastyear))+ 'gagr'
ror = 15 #How many questions asked
x = 0 #Do not change

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

def getSheet():
    #Scrapes information off of the quanatiative
    global mainList
    mainList = []

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1C8Jgf7W5VTzNBMeYhkVsjFx3g6fqF8MzqdUfIvHAMDE' #Google Sheet ID
    rangeName = 'B2:P' #Range
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    #for row in values:
        #for x in range(0, len(row)): #Range of Rows
            #mainList.append(str(row[x]))
    for x in range(0, len(values)):
        for y in range(0, ror):
            try:
                mainList.append(values[x][y])
            except:
                break
def findInfo(sendy, y):
    #Makes the List
    x = y
    z = 0 #No not change
    for z in range(0, 5000):
        try:
            sendy.append(mainList[x])
            x = x + ror
        except:
            return(sendy)

def perCal(y):
    y = float(y)
    y = y * 100
    round(y,2)
    y = (str(y)+'%')
    return(y)

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

def singleTeamList():
    teamList = getTeamNumber()
    checked = []
    for x in range(0, len(teamList)):
        if teamList[x] in checked:
            continue
        checked.append(teamList[x])
    return(checked)

def nullcatch(x):
    if x == '':
        x = 0
    return(x)

def getScoutingData():
    scoutingDataList = []
    x = 0
    for x in range(0, len(getTeamNumber())):
        scoutingData = {}
        add = {
        'matchesIn':(getList(1)[x]),
        'Scouters':(getList(2)[x]),
        'startingPosition':(getList(3)[x]),
        'A-Line':(getList(4)[x]),
        'A-High':(getList(5)[x]),
        'A-Low':(getList(6)[x]),
        'teleopHighGoals':(getList(7)[x]),
        'teleopLowGoals':(getList(8)[x]),
        'vaults':(getList(9)[x]),
        'playStyles':(getList(10)[x]),
        'usefull':(getList(11)[x]),
        'rating':(getList(12)[x]),
        'climb':(getList(13)[x]),
        'response':(getList(14)[x])}
        scoutingData.update(add)
        scoutingDataList.append(scoutingData)
    return(scoutingDataList)

def teamDictMaker():
    scoutingData = getScoutingData()
    #Puts all the Team Information into a dictionary
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
            add1 = teamDict[teamList[x]]
            add2 = scoutingData[x]
            matchList = []
            scouterList = []
            positionList = []
            autoLineList = []
            climbList = []
            styleList = []
            aLowList = []
            aHighList = []
            matchList.append(add1['matchesIn'])
            matchList.append(add2['matchesIn'])
            scouterList.append(add1['Scouters'])
            scouterList.append(add2['Scouters'])
            positionList.append(add1['startingPosition'])
            positionList.append(add2['startingPosition'])
            autoLineList.append(add1['A-Line'])
            autoLineList.append(add2['A-Line'])
            styleList.append(add1['playStyles'])
            styleList.append(add2['playStyles'])
            climbList.append(add1['climb'])
            climbList.append(add2['climb'])
            aLowList.append(str(add1['A-Low']))
            aLowList.append(str(add2['A-Low']))
            aHighList.append(str(add1['A-High']))
            aHighList.append(str(add2['A-High']))
            add3 = {
            'matchesIn':(matchList),
            'Scouters':(scouterList),
            'startingPosition':(positionList),
            'A-Line':(autoLineList),
            'A-Low':(aLowList),
            'A-High':(aHighList),
            'teleopHighGoals':(str(int(nullcatch(add1['teleopHighGoals']))+(int(nullcatch(add2['teleopHighGoals']))))),
            'teleopLowGoals':(str(int(nullcatch(add1['teleopLowGoals']))+(int(nullcatch(add2['teleopLowGoals']))))),
            'vaults':(str(int(nullcatch(add1['vaults']))+(int(nullcatch(add2['vaults']))))),
            'usefull':(str(int((add1['usefull']))+(int(add2['usefull'])))),
            'playStyles':(styleList),
            'rating':(str(int((add1['rating']))+(int(add2['rating'])))),
            'climb':(climbList),
            'response':((add1['response'])+'; '+(add2['response'])),
            'matchesRec':(str(int(checked.count(teamList[x]))))}
            add = {teamList[x]: (add3)}
        else:
            checked.append(teamList[x])
            y = scoutingData[x]
            add2 = {
            'matchesIn':(y['matchesIn']),
            'Scouters':(y['Scouters']),
            'startingPosition':(y['startingPosition']),
            'A-Line':(y['A-Line']),
            'A-Low':(y['A-Low']),
            'A-High':(y['A-High']),
            'teleopHighGoals':nullcatch(y['teleopHighGoals']),
            'teleopLowGoals':nullcatch(y['teleopLowGoals']),
            'vaults':nullcatch(y['vaults']),
            'playStyles':(y['playStyles']),
            'usefull':(y['usefull']),
            'rating':(y['rating']),
            'climb':(y['climb']),
            'response':(y['response']),
            'matchesRec':(1)}
            add = {(teamList[x]): (add2)}
        teamDict.update(add)
    return(teamDict)

def getHistoricData(teamBlankNumber):
    #Collects Historic Data
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
    year = date.today().year
    Age = rookieY - year
    return Age

def weightHistory():
    #Gives weights to all data collected historicaly
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
    try:
        round(y,0)
        int(y)
    except:
        pass
    return(y)

def catcher(x,x1,y,y1,z,z1,xy,xz,yz):
    if x > y:
        if x > z:
            return(x1)
    if y > x:
        if y > z:
            return(y1)
    if z > x:
        if z > y:
            return(z1)
    if x == y:
        return(xy)
    if x == z:
        return(xz)
    if y == z:
        return(yz)

def weightActive():
    #Gives a weights to all data collected activley
    weightActiveList = []
    typeList = []
    playList = []
    highAvList = []
    lowAvList = []
    vaultAvList = []
    climbAvList = []
    startingList = []
    avALine = []
    avAHigh = []
    avALow = []
    for x in range(0, len(singleTeamList())):
        weightAutoActions = 0
        teamList = singleTeamList()[x]
        matches = int(teamDict[teamList]['matchesRec'])
        #getAutoActions = teamDict[teamList]['Auto Actions']
        playLists = teamDict[teamList]['playStyles']
        getTeleopHighGoals = int(teamDict[teamList]['teleopHighGoals'])
        getTeleopLowGoals = int(teamDict[teamList]['teleopLowGoals'])
        getVaults = int(teamDict[teamList]['vaults'])
        getUsefull = int(teamDict[teamList] ['usefull'])
        climbList = teamDict[teamList]['climb']
        getRating = int(teamDict[teamList]['rating'])
        autoLow = ((teamDict[teamList]['A-Low'].count('1')+(teamDict[teamList]['A-Low'].count('2'))))
        autoHigh = ((teamDict[teamList]['A-High'].count('1')+(teamDict[teamList]['A-High'].count('2'))))
        autoCross = (teamDict[teamList]['A-Line'].count('Yes'))
        doubleLow = (teamDict[teamList]['A-Low'].count('2'))
        doubleHigh = (teamDict[teamList]['A-High'].count('2'))
        aggressivePlays = playLists.count('Agressive')
        defensivePlays = playLists.count('Defensive')
        bothPlays = playLists.count('Both')
        unknownPlays = playList.count('Inconclusive')
        positions = (teamDict[teamList]['startingPosition'])
        right = positions.count('R')
        middle = positions.count('M')
        left = positions.count('L')
        noShows = positions.count('No Show')

        #playStyle of Robot
        playStyle = catcher(aggressivePlays,'Agressive',defensivePlays,'Defensive',bothPlays,'Adaptable','Adaptable','Adaptable','Adaptable')

        #Favorite Position of Robot
        start = catcher(right,'Right',middle,'Middle',left,'Left','Inconclusive','Inconclusive','Inconclusive')

        #Type of Robot
        if getTeleopHighGoals > getTeleopLowGoals:
            if getTeleopHighGoals > getVaults:
                type = 'High Goal Shooter'
                if (getTeleopHighGoals-3) > getVaults:
                    if (getTeleopHighGoals-3) > getTeleopLowGoals:
                        type = 'Hard High Shooter'
        elif getTeleopLowGoals > getTeleopHighGoals:
            if getTeleopLowGoals > getVaults:
                type = 'Low Goal Shooter'
                if (getTeleopLowGoals-4) > getTeleopHighGoals:
                    if (getTeleopLowGoals-4) > getVaults:
                        type = 'Hard Low Shooter'
        elif getVaults > getTeleopHighGoals:
            if getVaults > getTeleopLowGoals:
                type = 'Vault Main'
                if (getVaults-4) > getTeleopHighGoals:
                    if (getVaults-4) > getTeleopLowGoals:
                        type = 'Hard Vault Main'
        elif getTeleopLowGoals == getTeleopHighGoals:
            type = 'High & Low Shooter'
        elif getTeleopLowGoals == getVaults:
            type = 'Vault & Low Goal Shooter'
        elif getTeleopHighGoals == getVaults:
            type = 'Vault & High Goal Shooter'
        elif getTeleopLowGoals == getTeleopHighGoals:
            if getTeleopLowGoals == getVaults:
                type = 'Mix'
        if getVaults == 0:
            if getTeleopHighGoals == 0:
                if getTeleopLowGoals == 0:
                    type = 'Vegetable'

        #Auto Data weighting
        autoCross = ((autoCross)/(matches))
        if autoCross >= 1:
            if autoCross >= 0.75:
                weightAutoActions = weightAutoActions + 3
        if autoLow >= 1:
            autoLow = autoLow / matches
            if autoLow >= 0.4:
                weightAutoActions = weightAutoActions + 6
        if autoHigh >= 1:
            autoHigh = autoHigh / matches
            if autoHigh >= 0.15:
                weightAutoActions = weightAutoActions + 8
        if doubleLow >= 1:
            doubleLow = doubleLow / matches
            if doubleLow >= 0.15:
                weightAutoActions = weightAutoActions + 3
        if doubleHigh >= 1:
            doubleHigh = doubleLow / matches
            if doubleLow >= 0.1:
                weightAutoActions = weightAutoActions + 4

        teleopScore = (((getVaults*1.75)+(getTeleopLowGoals*3)+(getTeleopHighGoals*3.5))/matches)
        getUsefull = ((getUsefull / matches)-1)
        getRating = ((getRating / matches)-2)

        if climbList.count('Yes') >= 1:
            weightClimber = (((climbList.count('Yes'))*(4))/(matches))
        else:
            weightClimber = 0

        active = (
        int(weightAutoActions) +
        int(teleopScore) +
        int(getUsefull) +
        int(getRating) +
        int(weightClimber))
        if active < 0:
            active = 0
            type = 'Vegetable'
        active = whole(active)
        weightActiveList.append(active)
        typeList.append(type)
        playList.append(playStyle)
        highAvList.append(str(round(getTeleopHighGoals/matches,1)))
        lowAvList.append(str(round(getTeleopLowGoals/matches,1)))
        vaultAvList.append(str(round(getVaults/matches,1)))
        climbAvList.append(str(round(climbList.count('Yes')/matches,1)))
        startingList.append(start)
        avALine.append(str(round(autoCross,1)))
        avALow.append(str(round(autoLow,1)))
        avAHigh.append(str(round(autoHigh,1)))
    return(weightActiveList, typeList, playList, highAvList,
    lowAvList, vaultAvList, startingList, avALine, avALow, avAHigh, climbAvList)

def dataAnalysis():
    teamList = singleTeamList()
    aData = weightActive()
    #hData = weightHistory()
    x = 0
    score = 0
    printData = []
    for x in range(0, len(teamList)):
        score = int(aData[0][x])
        type = aData[1][x]
        playStyle = aData[2][x]
        y = teamDict[teamList[x]]
        score = whole(score)
        add = {
        'score':(int(score)),
        'type':(type),
        'playStyle':(playStyle),
        'matchesIn':(y['matchesIn']),
        'Scouters':(y['Scouters']),
        'startingPosition':(aData[6][x]),
        'Average A-Line':perCal(aData[7][x]),
        'Average A-Low':perCal(aData[8][x]),
        'Average A-High':perCal(aData[9][x]),
        'teleopHighGoals':(aData[3][x]),
        'teleopLowGoals':(aData[4][x]),
        'vaults':(aData[5][x]),
        'climb':perCal(aData[10][x]),
        'response':(y['response']),
        'matchesRec':(y['matchesRec'])
        }
        printData.append(add)
    return(printData)

def getLeaderboard():
    #Creates a leaderboard
    teamList = singleTeamList()
    getLeaderboard = {}
    data = dataAnalysis()
    for x in range(0, len(teamList)):
        add = {(teamList[x]): (data[x])}
        getLeaderboard.update(add)
    return(getLeaderboard)

def finalPrint():
    #Puts all data collected in a Panda Dataframe
    leaderboard = getLeaderboard()
    data = []
    checked = singleTeamList()
    print('Summary of all Teams')
    for x in range (0, len(checked)):
        score = (str(leaderboard[checked[x]]['score']))
        type = (str(leaderboard[checked[x]]['type']))
        playStyle = (str(leaderboard[checked[x]]['playStyle']))
        response = (str(leaderboard[checked[x]]['response']))
        add = [score,type,playStyle,response]
        data.append(add)
    df = pd.DataFrame(data,index=[checked],columns=['Score','Type','Play Style','Reponse'])
    print(df)
    print()
    print('All Data Collected by Team 6925\'s scouts.')
    for x in range (100):
        print('Lookup more Information')
        print()
        lookup = input('Team #: ')
        try:
            y = leaderboard[lookup]
            data2 = [[
            str(y['score']),
            str(y['type']),
            str(y['startingPosition']),
            str(y['playStyle']),
            str(y['vaults']),
            str(y['teleopLowGoals']),
            str(y['teleopHighGoals']),
            str(y['climb']),
            str(y['Average A-Line']),
            str(y['Average A-Low']),
            str(y['Average A-High']),
            str(y['response']),
            ]]
            df2 = pd.DataFrame(data2,index=[lookup],columns=['Score','Type','Start',
            'Play Style','Mean Vault','Mean Low','Mean High','Climb Success','Mean A-Line',
            'Mean A-Low','Mean A-High','Response'])
            print(df2)
        except KeyError:
            if lookup == '':
                print('Actually put something in.')
            else:
                print('Could not find team '+str(lookup)+'.')
        except:
            print('An error occured!')
        print()

if __name__ == '__main__':
    get_credentials()
    getSheet()
    teamDictMaker()
    finalPrint()
