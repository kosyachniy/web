"""
Google Documents functionality for the API
"""

from libdev.cfg import cfg
import gspread
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
)


credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    cfg('google.credentials'), SCOPES,
)
client = gspread.authorize(credentials)


def open_sheets(key):
    """ Open a spreadsheet """
    return client.open_by_key(key).worksheets()

def create_sheets(title, mail):
    """ Create a spreadsheet """
    sheet = client.create(title)
    sheet.share(mail, perm_type='user', role='writer')
    return sheet.url
