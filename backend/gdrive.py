import os
import json
import gspread
import pandas as pd
from backend.secrets import get_secret, SECRETS


def get_data():
    url = get_secret(SECRETS.GOOGLE_SHEET)
    creds = get_secret(SECRETS.GOOGLE_CRED)
    gdrive_client = gspread.authorize(creds)
    data_sheet = gdrive_client.open_by_url(url)
    data = data_sheet.get_worksheet(0).get_all_records()    
    return data


def get_dataframe():
    data = get_data()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df
