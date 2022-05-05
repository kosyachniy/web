"""
Google Documents functionality for the API
"""

# pylint: disable=import-error
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ],
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def create(name, sheets, mail):
    """ Create a document """

    spreadsheet = service.spreadsheets().create(
        body = {
            'properties': {
                'title': name,
                'locale': 'ru_RU',
            },
            'sheets': [{
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': i,
                    'title': sheet,
                    'gridProperties': {
                        'rowCount': 100,
                        'columnCount': 30,
                    },
                },
            } for i, sheet in enumerate(sheets)],
        },
    ).execute()

    spreadsheet_id = spreadsheet['spreadsheetId']
    print(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

    drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    drive_service.permissions().create(
        fileId = spreadsheet_id,
        body = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': mail,
        },
        fields = 'id'
    ).execute()
