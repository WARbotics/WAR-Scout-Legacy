from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import tbapy
import httplib2
import os
import requests
import numpy
import pandas
import matplotlib
from datetime import date
import texttable as tt
key = "wri5PWmHJw5O9TrdMtUrWQktTK9J0eQqg1DuLMeyS55T5F2r2nEn0qWRls7W0Y2P"
tba = tbapy.TBA(key)
class WARScout:
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
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

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
        try:

            """Shows basic usage of the Sheets API.

            Creates a Sheets API service object and prints the names and majors of
            students in a sample spreadsheet:
            https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
            """
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                            'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                      discoveryServiceUrl=discoveryUrl)

            spreadsheetId = '1C8Jgf7W5VTzNBMeYhkVsjFx3g6fqF8MzqdUfIvHAMDE'
            rangeName = sheet + '!B2:b'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for row in values:
                    list.append(int(row[0]))
                    list.append(int(row[1]))
        except:
            print('You got beaned no data found kiddo')
    key = ""
    tba = tbapy.TBA(key)
    event = "PCH District Gainesville Event"
    tab = tt.Texttable()
    def status():
        #figuring out if TBA is actually online
        statusCheck = tba.status()
        if statusCheck['is_datafeed_down'] == False
    else:
        print ('Team Blue alliance systems are down')
            exit()

    def getYear():
        #collecting currect year
        year = date.today().year
    def __init__():
        print("WAR botics FRC scouting script")
    teamNumber = list[0]
    def getTeamData(teamNumber):
        #collecting data
        mainTeam = tba.team(teamNumber, False)
        nickName = mainTeam['nickname']
        teamWebsite = mainTeam['website']
        rookieYear = mainTeam['rookie_year']
    def teamAge(rookieYear, year):
        #clean this mess
        rookieYear - year = age


if __name__ == '__main__':
    w = WARScout()
    header = ['Team Number', 'NickName', 'Team Age']
    tab.header(header)
    tab.add_row(teamNumber)
    tab.add_row(w.getTeamData(teamNumber).nickName)
    tab.add_row(w.teamAge(getTeamData(teamNumber).rookieYear))
    print tab.draw()
