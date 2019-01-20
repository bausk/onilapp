import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os



scope = ['https://spreadsheets.google.com/feeds']
url = 'https://docs.google.com/spreadsheets/d/1gjzWEyK36pd5oY6q_oQYvv15yTFc4eGUqIAYkHJLPbs'

creds = None
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        './credentials/googlekey.json', scope)
except:
    json_data = os.environ['GSPREAD_CREDENTIALS']
    creds = ServiceAccountCredentials.from_json(json_data)

def get_data():
    gdrive_client = gspread.authorize(creds)
    data_sheet = gdrive_client.open_by_url(url)
    data = data_sheet.get_worksheet(0).get_all_records()
    return data
