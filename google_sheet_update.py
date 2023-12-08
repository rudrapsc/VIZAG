from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime,date
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1AQ6TgA_hm2bocR8eEwC9WLBDc7vScjg2ZhKAwAvIIBQ'
SAMPLE_RANGE_NAME = 'Sheet1'
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json",SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.json","w") as token:
        token.write(creds.to_json())
service = build("sheets","v4", credentials=creds)
sheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = sheet['sheets']
today = date.today()
today = str(today)
# Print sheet names
for sheet in sheets:
    sheet_title = sheet['properties']['title']
    if sheet_title == today:
        break
else:
    
# Create a new sheet with today's date as the name
    request_body = {
        'requests': [
            {
                'addSheet': {
                    'properties': {
                        'title': today
                    }
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(spreadsheetId= SPREADSHEET_ID , body=request_body).execute()
# 
def update_sheet(text,cam):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:F').execute()
    value = result.get('values',[])
    print(value)
    value_exist_1 = any(text in row for row in value)
    pass
