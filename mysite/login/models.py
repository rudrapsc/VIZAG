from django.db import models
from datetime import datetime
class LadleInfo(models.Model):
    name = models.CharField(max_length=100)
    stop_point_no=models.IntegerField(default=0)
    stop_point_work=models.CharField(max_length=500,default="hii")
    min_temp=models.IntegerField(default=0)
    max_temp=models.IntegerField(default=0)
    turn_around_time=models.IntegerField(default=0)

class Ladle(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100,default="hii")
    rounds_daily=models.IntegerField(default=0)
    rounds_life=models.IntegerField(default=0)

class Comment(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=100,default="NO COMMENT")

class LadleUpdateRoomWise(models.Model):
    name = models.CharField(max_length=100)
    date= models.DateField(default=datetime.today().date())
    entry_time=models.CharField(max_length=500)
    room=models.CharField(max_length=500)
    exit_time=models.CharField(max_length=500)
    stop_points=models.CharField(max_length=500,default="hii")
    first_time=models.CharField(max_length=500,default="hii")
    entry_room=models.CharField(max_length=500,default="hii")
    turn_overtime=models.CharField(max_length=500,default="[]")
    turns=models.IntegerField(default=0)

class EntriesAdded(models.Model): 
    name = models.CharField(max_length=100)
    date= models.DateField(default=datetime.today().date())
    count = models.IntegerField()

class User(models.Model): 
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
 
class Admin(models.Model): 
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
       
