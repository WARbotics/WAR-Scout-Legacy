from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


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

        spreadsheetId = '1-CeZMc6wb3X-L0ljsQIrLODhHt-SPJBmvi8BDEdz2OA'
        rangeName = sheet + '!A2:b'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                list.append(int(row[0]))
                list.append(int(row[1]))
        global endh
        global endm
        getEndh = list.index(99) - 2
        getEndm = list.index(99) - 1
        endh = list[getEndh]
        endm = list[getEndm]
    except:
        if sheet == 'Current':
            list = [8,0,8,30,8,35,9,16,9,21,10,2,10,7,10,48,10,53,
                    11,34,11,39,12,4,12,9,12,50,12,55,13,36,13,41,
                    14,22,14,27,14,57,15,35,99,99]
        if sheet == 'CurrentF':
            list = [8,0,8,30,8,35,9,19,9,24,10,8,10,16,11,0,
                    11,5,11,49,11,54,12,19,12,24,13,8,13,16,14,0,
                    14,5,14,49,15,25,99,99]
        print('Error')
            
