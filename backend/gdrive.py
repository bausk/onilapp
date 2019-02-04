import os
import json
import gspread
from backend.secrets import get_secret, SECRETS


def get_data():
    url = get_secret(SECRETS.GOOGLE_SHEET)
    creds = get_secret(SECRETS.GOOGLE_CRED)
    gdrive_client = gspread.authorize(creds)
    data_sheet = gdrive_client.open_by_url(url)
    data = data_sheet.get_worksheet(0).get_all_records()
    return data
