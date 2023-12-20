
from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from login.models import *
import cv2
import asyncio
import websockets
import base64
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
from django.contrib.auth import logout
# from _future_ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime,date
import numpy as np

from mysite.tasks import add
from mysite.otp import send_email


def sheet():
    entriesadded=EntriesAdded.objects.filter(name='LadleUpdateRoomWise')
    count=entriesadded[0].count
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
            flow = InstalledAppFlow.from_client_secrets_file(r"C:\Users\jaink\Desktop\LADLE TRACKER\mysite\mysite\credentials.json",SCOPES)
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

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:G').execute()
    value = result.get('values',[])
    value = np.array(value)
    value=value[count:]
    ladleinfo=LadleInfo.objects.all()
    ladles=[]
    for x in value:
        ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=x[0],date=datetime.today().date())
        if len(ladleupdateroomwise)==0:
            name = x[0]
            room=[]
            entry_time=[]
            exit_time=[]
            stop_points=[]
            entry_room=x[3]
            turn_overtime=x[2]
            first_time=x[4]
            if x[0]==name:
                room.append(x[3])
                entry_time.append(x[4])
                exit_time.append(x[5])
                string=""
                for i in x[6]:
                    if i==",":
                        stop_points.append(string)    
                        string=""
                    else:
                        string=string+i  
                stop_points.append(string)  
                en=LadleUpdateRoomWise(name=name,entry_time=entry_time,room=room,exit_time=exit_time,stop_points=stop_points,entry_room=entry_room,first_time=first_time)
                en.save()
                en2=LadleInfo(name=name)
                en2.save()
                en3=Comment(name=name)
                en3.save()
                count=count+1
        else:
            name_2 = x[0]
            room=[]
            entry_time=[]
            exit_time=[]
            stop_points_1=[]
            stop_points_2=[]
            turn_overtime=[]
            string=""
            for z in ladleupdateroomwise:
                for y in z.turn_overtime:
                    if y=="'" and string!="":
                        turn_overtime.append(string)    
                        string=""
                    elif  y!="'" and y!="[" and y!="]" and y!=",":
                        string=string+y 
            for z in ladleupdateroomwise:
                if z.entry_room==x[3]:
                    co=z.turns+1
                    timestamp_format = "%H:%M:%S"
                    turn_overtime.append(str(datetime.strptime(x[4], timestamp_format)-datetime.strptime(z.first_time, timestamp_format)))
                    for a in turn_overtime:
                        if a==" ":
                            turn_overtime.remove(a)
                    LadleUpdateRoomWise.objects.filter(name=name_2,date=datetime.today().date()).update(turns=co,turn_overtime=turn_overtime,first_time=x[4])
                    break
            string=""
            for z in ladleupdateroomwise:
                for y in z.stop_points:
                    if y=="'" and string!="":
                        stop_points_1.append(string)    
                        string=""
                    elif  y!="'" and y!="[" and y!="]" and y!=",":
                        string=string+y  
            for a in stop_points_1:
                    if a==" ":
                        stop_points_1.remove(a)
            string=""
            for z in ladleupdateroomwise:
                for y in z.room:
                    if y=="'" and string!="":
                        room.append(string)    
                        string=""
                    elif  y!="'" and y!="[" and y!="]" and y!=",":
                        string=string+y     
            string=""
            for z in ladleupdateroomwise:
                for y in z.entry_time:
                    if y=="'" and string!="":
                        entry_time.append(string)    
                        string=""
                    elif  y!="'" and y!="[" and y!="]" and y!=",":
                        string=string+y 
            string=""
            for z in ladleupdateroomwise:
                for y in z.exit_time:
                    if y=="'" and string!="":
                        exit_time.append(string)    
                        string=""
                    elif  y!="'" and y!="[" and y!="]" and y!=",":
                        string=string+y 
            if x[0]==name_2:
                room.append(x[3])
                entry_time.append(x[4])
                exit_time.append(x[5])
                
                string=""
                for i in x[6]:
                    if i==",":
                        stop_points_2.append(string)    
                        string=""
                    else:
                        string=string+i  
                stop_points_2.append(string)
                stop_points_3=stop_points_1+stop_points_2
                datetime_objects = [datetime.strptime(timestamp, "%H:%M:%S") for timestamp in stop_points_3]
                sorted_datetime_objects = sorted(datetime_objects)
                sorted_timestamps = [datetime.strftime(dt, "%H:%M:%S") for dt in sorted_datetime_objects]
                for a in room:
                    if a==" ":
                        room.remove(a)
                for a in entry_time:
                    if a==" ":
                        entry_time.remove(a)
                for a in exit_time:
                    if a==" ":
                        exit_time.remove(a)
                LadleUpdateRoomWise.objects.filter(name=name_2,date=datetime.today().date()).update(entry_time=entry_time,room=room,exit_time=exit_time,stop_points=sorted_timestamps)
                count=count+1
                    
    EntriesAdded.objects.filter(name="LadleUpdateRoomWise").update(count=count)
    return count
    
def home_2(request):
    ans=sheet()
    ladleinfo=LadleInfo.objects.all()
    return render(request,"homepage.html",{'ladleinfo':ladleinfo})
def comment(request):
    return HttpResponse("homepage.html")
def login(request):
    if request.method == 'POST':
        user_username = request.POST.get('user_username')
        user_password = request.POST.get('user_password')
        user=User.objects.all()
        for x in user:
            if x.username==user_username and x.password==user_password:
                return redirect('/homepage')
    return render(request,"login.html")

def admin_login(request):
    if request.method == 'POST':
        admin_username = request.POST.get('admin_username')
        admin_password = request.POST.get('admin_password')
        admin=Admin.objects.all()
        for x in admin:
            if x.username==admin_username and x.password==admin_password:
                return render(request,"admin_page.html")
    return render(request,"admin_login.html")
def user_logout(request):
    logout(request)
    return redirect("/")

def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        users=User.objects.all()
        for i in users:
            if i.name==name or i.username==username:
                return render(request,"create_user.html")    
        en=User(name=name,username=username,password=password)
        en.save()
    return render(request,"create_user.html")

def send_mail(request):
    ladleinfo=LadleInfo.objects.all()
    ladleupdateroomwise=LadleUpdateRoomWise.objects.all()
    ladles=[]
    rooms=[]
    string=""
    for x in ladleupdateroomwise:
        for y in x.room:
            if y=="'" and string!="":
                rooms.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y 
        for a in rooms:
            if a==" ":
                rooms.remove(a)  
        length=len(rooms) 
        if length!=0:
            if rooms[0]!=rooms[length-1]:
                ladles.append(x.name)
    print(str(ladles))
    send_email(str(ladles))
    return render(request,"homepage.html",{'ladleinfo':ladleinfo})

def add_ladle(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # type = request.POST.get('type')
        rounds_daily = request.POST.get('rounds_daily')
        rounds_life = request.POST.get('rounds_life')
        en=Ladle(name=name,rounds_daily=rounds_daily,rounds_life=rounds_life)
        en.save()
        en2=LadleInfo(name=name)
        en2.save()
        en3=Comment(name=name)
        en3.save()
    return render(request,"add_ladle.html")

def detail(request):
    ladlename = request.GET.get('ladlename')
    date='default'
    if request.method == 'POST':
        date = request.POST.get('date')
    if date=='default':
        date=datetime.today().date()
    ladleupdateroomwise1=LadleUpdateRoomWise.objects.filter(name=ladlename,date=date)
    ladleinfo=LadleInfo.objects.filter(name=ladlename)
    room=[]
    entry_time=[]
    exit_time=[]
    stop_points=[]
    stop_point_work=[]
    turn_overtime=[]
    string=""
    for x in ladleupdateroomwise1:
        for y in x.stop_points:
            if y=="'" and string!="":
                stop_points.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise1:
        for y in x.entry_time:
            if y=="'" and string!="":
                entry_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise1:
        for y in x.exit_time:
            if y=="'" and string!="":
                exit_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y 
    string=""
    for x in ladleupdateroomwise1:
        for y in x.room:
            if y=="'" and string!="":
                room.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y
    string=""
    for x in ladleupdateroomwise1:
        for y in x.turn_overtime:
            if y=="'" and string!="":
                turn_overtime.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y    
    for a in room:
        if a==" ":
            room.remove(a)
    for a in turn_overtime:
        if a==" ":
            turn_overtime.remove(a)
    for a in stop_points:
        if a==" ":
            stop_points.remove(a)
    for a in entry_time:
        if a==" ":
            entry_time.remove(a)
    for a in exit_time:
        if a==" ":
            exit_time.remove(a)
    list1 = list(zip(room,entry_time,exit_time))
    
    average_turnaround_time=0
    data=[]
    labels=[]
    no_of_rounds=0
    list2=list(zip(stop_points,stop_point_work))
    for x in ladleupdateroomwise1: 
        no_of_rounds=x.turns
    for i in range(1,int(no_of_rounds)+1):
        labels.append('Round '+str(i))
    if no_of_rounds!=0:
        for x in turn_overtime:
            dt_object = datetime.strptime(str(x), "%H:%M:%S")
            hour = dt_object.hour
            minute = dt_object.minute
            second = dt_object.second
            data.append(int((hour*60*60)+(60*minute)+second))
            average_turnaround_time = average_turnaround_time+int((hour*60*60)+(60*minute)+second)
        hours, remainder = divmod(average_turnaround_time/no_of_rounds, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_turnaround_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    return render(request,"detail.html",{'ladlename':ladlename,'date':date,'list1':list1,'list2':list2,'turn_overtime':turn_overtime,'data':data,'labels':labels,'no_of_rounds':no_of_rounds,'average_turnaround_time':average_turnaround_time})

def find(request):
    time=""
    dropdown=""
    if request.method == 'POST':
        time = request.POST.get('time')
        dropdown = request.POST.get('dropdown')
    ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=dropdown)
    ladleinfo=LadleInfo.objects.all()
    ladles=[]
    for x in ladleinfo:
        ladles.append(x.name)
    entry_time=[]
    room=[]
    exit_time=[]
    string=""
    for x in ladleupdateroomwise:
        for y in x.entry_time:
            if y=="'" and string!="":
                entry_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    string=""
    for x in ladleupdateroomwise:
        for y in x.room:
            if y=="'" and string!="":
                room.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise:
        for y in x.exit_time:
            if y=="'" and string!="":
                exit_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    for a in room:
        if a==" ":
            room.remove(a)
    for a in entry_time:
        if a==" ":
            entry_time.remove(a)
    for a in exit_time:
        if a==" ":
            exit_time.remove(a)            
    time=time
    type="torpido"
    result="none"
    
    task = list(zip(entry_time,exit_time,room)) 
    for x in task:
        if datetime.strptime(time,"%H:%M:%S")>=datetime.strptime(x[0],"%H:%M:%S") and datetime.strptime(time,"%H:%M:%S")<=datetime.strptime(x[1],"%H:%M:%S"):
            result=x[2]
            break
        elif datetime.strptime(time,"%H:%M:%S")<datetime.strptime(x[0],"%H:%M:%S"):
            result="TOWARDS" + x[2]
            break
    
    return render(request,"find.html",{'ladles':ladles,'dropdown':dropdown,'time':time,'result':result})

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_frames_2():
    video_capture = cv2.VideoCapture(1)
    while True:
        # Read a frame from the webcam
        success, frame = video_capture.read()

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        # Yield the frame bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def get_frames():
    laptop_camera = cv2.VideoCapture(0) 
    external_camera = cv2.VideoCapture(1)
    while True:
        # Read frames from the cameras
        success_laptop, frame_laptop = laptop_camera.read()
        success_external, frame_external = external_camera.read()

        # Convert the frames to JPEG format
        ret_laptop, jpeg_laptop = cv2.imencode('.jpg', frame_laptop)
        ret_external, jpeg_external = cv2.imencode('.jpg', frame_external)

        frame_bytes_laptop = jpeg_laptop.tobytes()
        frame_bytes_external = jpeg_external.tobytes()

        # Yield the frame bytes from both cameras
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_laptop + b'\r\n\r\n',
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_external + b'\r\n\r\n'
        )

@gzip.gzip_page
def live_feed(request):
    return StreamingHttpResponse(get_frames(), content_type="multipart/x-mixed-replace;boundary=frame")

def camera(request):
    return render(request,"camera.html")
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
# @gzip.gzip_page
# def video_feed_2(request):
#     return StreamingHttpResponse(generate_frames_2(),content_type="multipart/x-mixed-replace;boundary=frame")

async def receive_video():
    uri = "ws://192.168.1.174:8765"  
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                # Receive base64-encoded image data from the WebSocket server
                data = await websocket.recv()
                
                # Decode base64 and convert to NumPy array
                buffer = base64.b64decode(data)
                image = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)

                # Display the received frame
                cv2.imshow("Video Stream", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed with error.")
                break
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed normally.")
                break

def all(request):
    ladleinfo=LadleInfo.objects.all()
    ladle=[]
    data_room=[]
    data_entry_time=[]
    data_exit_time=[]
    for x in ladleinfo:
        ladle.append(x.name)
        room=[]
        entry_time=[]
        exit_time=[]
        # print(x.name)
        ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=x.name,date=datetime.today().date())
        string=""
        # for d in ladleupdateroomwise:
        #     print(d.name)
    
        for z in ladleupdateroomwise:
            for y in z.room:
                if y=="'" and string!="":
                    room.append(string)    
                    string=""
                elif  y!="'" and y!="[" and y!="]" and y!=",":
                    string=string+y 
        string="" 
        for z in ladleupdateroomwise:
            for y in z.entry_time:
                if y=="'" and string!="":
                    entry_time.append(string)    
                    string=""
                elif  y!="'" and y!="[" and y!="]" and y!=",":
                    string=string+y 
        string="" 
        for z in ladleupdateroomwise:
            for y in z.exit_time:
                if y=="'" and string!="":
                    exit_time.append(string)    
                    string=""
                elif  y!="'" and y!="[" and y!="]" and y!=",":
                    string=string+y   
        for a in room:
            if a==" ":
                room.remove(a)
        
        for a in entry_time:
            if a==" ":
                entry_time.remove(a) 
        for a in exit_time:
            if a==" ":
                exit_time.remove(a) 
        length=len(room)
        if length!=0:
            for i in range(length-1,length):
                data_room.append(room[i])
                data_entry_time.append(entry_time[i])
                data_exit_time.append(exit_time[i])
        # print(ladle)
        data = list(zip(ladle,data_entry_time,data_room,data_exit_time))
        da=datetime.today().date()
    return render(request,"all_data.html",{'data':data,'da':da})

def add_comment(request):
    if request.method == 'POST':
        comment_ = request.POST.get('comment')
        dropdown = request.POST.get('dropdown')
        print(comment_,dropdown)
        Comment.objects.filter(name=dropdown).update(comment=comment_)
    ladleinfo=LadleInfo.objects.all()
    ladles=[]
    turns=[]
    turn_over_times=[]
    comments=[]
    for x in ladleinfo:
        ladles.append(x.name)
        ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=x.name)
        comment=Comment.objects.filter(name=x.name)
        comments.append(comment[0].comment)
        turn=0
        turn_over_time=[]
        for y in ladleupdateroomwise:
            turn=turn+y.turns
            string=""
            for z in y.turn_overtime:
                if z=="'" and string!="":
                    turn_over_time.append(string)    
                    string=""
                elif  z!="'" and z!="[" and z!="]" and z!=",":
                    string=string+z
            for a in turn_over_time:
                if a==" ":
                    turn_over_time.remove(a) 
        average_turnaround_time=0
        for x in turn_over_time:
            dt_object = datetime.strptime(str(x), "%H:%M:%S")
            hour = dt_object.hour
            minute = dt_object.minute
            second = dt_object.second
            average_turnaround_time = average_turnaround_time+int((hour*60*60)+(60*minute)+second)
        hours, remainder = divmod(average_turnaround_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_turnaround_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)) 
        turn_over_times.append(average_turnaround_time)       
        turns.append(turn)
    status=[]
    for x in turns:
        if int(x)<=7:
            status.append(2)
        elif int(x)==8:
            status.append(1) 
        elif int(x)>8:
            status.append(0)   
    data = list(zip(ladles,turns,turn_over_times,status,comments))
    return render(request,"add_comment.html",{'data':data,'ladles':ladles})

def life(request):
    ladleinfo=LadleInfo.objects.all()
    ladles=[]
    turns=[]
    turn_over_times=[]
    comments=[]
    for x in ladleinfo:
        ladles.append(x.name)
        ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=x.name)
        comment=Comment.objects.filter(name=x.name)
        comments.append(comment[0].comment)
        turn=0
        turn_over_time=[]
        for y in ladleupdateroomwise:
            turn=turn+y.turns
            string=""
            for z in y.turn_overtime:
                if z=="'" and string!="":
                    turn_over_time.append(string)    
                    string=""
                elif  z!="'" and z!="[" and z!="]" and z!=",":
                    string=string+z
            for a in turn_over_time:
                if a==" ":
                    turn_over_time.remove(a) 
        average_turnaround_time=0
        for x in turn_over_time:
            dt_object = datetime.strptime(str(x), "%H:%M:%S")
            hour = dt_object.hour
            minute = dt_object.minute
            second = dt_object.second
            average_turnaround_time = average_turnaround_time+int((hour*60*60)+(60*minute)+second)
        hours, remainder = divmod(average_turnaround_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_turnaround_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)) 
        turn_over_times.append(average_turnaround_time)       
        turns.append(turn)
    status=[]
    for x in turns:
        if int(x)<=7:
            status.append(2)
        elif int(x)==8:
            status.append(1) 
        elif int(x)>8:
            status.append(0)   
    data = list(zip(ladles,turns,turn_over_times,status,comments))
    ladles_1=[]
    turns_1=[]
    turn_over_times_1=[]
    for x in ladleinfo:
        ladles_1.append(x.name)
        ladleupdateroomwise_1=LadleUpdateRoomWise.objects.filter(name=x.name,date=datetime.today().date())
        turn_1=0
        turn_over_time_1=[]
        for y in ladleupdateroomwise_1:
            turn_1=turn_1+y.turns
            string_1=""
            for z in y.turn_overtime:
                if z=="'" and string_1!="":
                    turn_over_time_1.append(string_1)    
                    string_1=""
                elif  z!="'" and z!="[" and z!="]" and z!=",":
                    string_1=string_1+z
            for a in turn_over_time_1:
                if a==" ":
                    turn_over_time_1.remove(a) 
        average_turnaround_time_1=0
        for x in turn_over_time_1:
            dt_object = datetime.strptime(str(x), "%H:%M:%S")
            hour = dt_object.hour
            minute = dt_object.minute
            second = dt_object.second
            average_turnaround_time_1 = average_turnaround_time_1+int((hour*60*60)+(60*minute)+second)
        hours, remainder = divmod(average_turnaround_time_1, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_turnaround_time_1 = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)) 
        turn_over_times_1.append(average_turnaround_time_1)       
        turns_1.append(turn_1)
    status_1=[]
    for x in turns_1:
        if int(x)<=7:
            status_1.append(2)
        elif int(x)==8:
            status_1.append(1) 
        elif int(x)>8:
            status_1.append(0) 
    data_1 = list(zip(ladles_1,turns_1,turn_over_times_1,status_1))
    return render(request,"life.html",{'data':data,'data_1':data_1})
            
        
# name = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     rounds_daily=models.IntegerField(default=0)
#     time_daily=models.IntegerField(default=0)
#     stop_point_work=models.CharField(max_length=500,default="hii")
#     min_temp=models.IntegerField(default=0)
#     max_temp=models.IntegerField(default=0)
#     turn_around_time=models.IntegerField(default=0)

# name = models.CharField(max_length=100)
#     stop_point_no=models.IntegerField(default=0)
#     stop_point_work=models.CharField(max_length=500,default="hii")
#     min_temp=models.IntegerField(default=0)
#     max_temp=models.IntegerField(default=0)
#     turn_around_time=models.IntegerField(default=0)