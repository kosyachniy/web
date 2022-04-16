"""
Google Documents functionality for the API
"""

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

    spreadsheetId = spreadsheet['spreadsheetId']
    print(f"https://docs.google.com/spreadsheets/d/{spreadsheetId}")

    driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    driveService.permissions().create(
        fileId = spreadsheetId,
        body = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': mail,
        },
        fields = 'id'
    ).execute()
