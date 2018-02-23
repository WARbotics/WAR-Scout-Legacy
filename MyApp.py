from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import tbapy
key = "wri5PWmHJw5O9TrdMtUrWQktTK9J0eQqg1DuLMeyS55T5F2r2nEn0qWRls7W0Y2P"
tba = tbapy.TBA(key)
class WARscout:
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
        getDay()
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
            rangeName = sheet + '!A2:j'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for row in values:
                    list.append(int(row[0]))
                    list.append(int(row[1]))

class Data:
    key = ""
    tba = tbapy.TBA(key)
    event = "PCH District Gainesville Event"
    def Status():
        tba.Status()
    def getStatus():
        return Status()
    def __init__():
        tba.event_rankings(event)
        print "WAR botics FRC scouting script"
    def getTeamData(teamNumber):
        # get the team number from google spread sheet
        yearTeam = tba.team_years(teamNumber)
        robotYear = tba.team_robots(teamNumber)
