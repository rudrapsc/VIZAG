from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime,date
import numpy as np
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
def update_sheet(numeric_parts,cam,time):
    room_cam = {
        69:"A",
        13:"B",
        71:"C",
        23:"D"
    }
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:F').execute()
    value = result.get('values',[])
    value = np.array(value)
    print(value)
    r,c = value.shape
    # room = str(cam)
    laddle_number = numeric_parts
    print("hello")
    print("laddle number is",laddle_number)
    print("time is",time)
    initial_room = room_cam[numeric_parts]
    initial_time = time
    entry = time
    exit =time
    # if value[r-1,3]==room :
    
    print("room is",room_cam[laddle_number])
    print("type of value is",type(value[r-1,3]))
    print("type of room cam np str is",type(np.str_(room_cam[laddle_number])))
    if ((value[r-1,3]==np.str_(room_cam[laddle_number])) and (value[r-1,0]==np.str_(laddle_number))):
        
        
        print("yes")
        
        new_value = [[exit]]
        request_body = { 
            'values':new_value
        }
        sheet1 = service.spreadsheets()
        sheet1.values().update(spreadsheetId=SPREADSHEET_ID,range=f'{today}!F{r}',valueInputOption='USER_ENTERED',body= request_body).execute()
        print(new_value)
    else:
        print("no")
        print("no2")
        new_value = [[laddle_number,initial_room,initial_time,room_cam[laddle_number],entry,exit]]
        print("before appending",new_value)
        request_body = { 
            'values':new_value
        }
        sheet1 = service.spreadsheets()
        sheet1.values().append(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:A',valueInputOption='USER_ENTERED',body= request_body).execute()
        print(new_value)        
