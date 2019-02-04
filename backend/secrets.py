import os
from enum import Enum
import json
from oauth2client.service_account import ServiceAccountCredentials


class SECRETS(Enum):
    GOOGLE_SHEET = 'GSHEETS_SHEET'
    GOOGLE_CRED = 'GSPREAD_CREDENTIALS'
    REDIS_HOST = 'REDIS_HOST'


def get_secret(secret):
    if secret == SECRETS.GOOGLE_CRED:
        creds = None
        scope = ['https://spreadsheets.google.com/feeds']
        try:
            json_data = json.loads(os.environ[SECRETS.GOOGLE_CRED.value])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(json_data, scope)
        except Exception:
            creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/googlekey.json', scope)
        return creds
    if secret == SECRETS.GOOGLE_SHEET:
        return os.environ[SECRETS.GOOGLE_SHEET.value]
    if secret == SECRETS.REDIS_HOST:
        return os.environ.get(SECRETS.REDIS_HOST.value)
