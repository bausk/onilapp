import os
from enum import Enum
import json
from oauth2client.service_account import ServiceAccountCredentials


class SECRETS(Enum):
    GOOGLE_SHEET = 1
    GOOGLE_CRED = 2
    REDIS_HOST = 3


def get_secret(secret):
    if secret == SECRETS.GOOGLE_CRED:
        creds = None
        scope = ['https://spreadsheets.google.com/feeds']
        try:
            json_data = json.loads(os.environ['GSPREAD_CREDENTIALS'])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(json_data, scope)
        except Exception:
            creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/googlekey.json', scope)
        return creds
    if secret == SECRETS.GOOGLE_SHEET:
        return os.environ['GSHEETS_SHEET']
    if secret == SECRETS.REDIS_HOST:
        return os.environ.get('REDIS_HOST')
