from django.contrib import admin
from login.models import LadleInfo , LadleUpdateRoomWise ,EntriesAdded,User,Admin,Ladle,Comment

class LadleInfoAdmin(admin.ModelAdmin):
    list_display=('name','stop_point_no','stop_point_work','min_temp','max_temp','turn_around_time')
admin.site.register(LadleInfo,LadleInfoAdmin)

class LadleAdmin(admin.ModelAdmin):
    list_display=('name','type','rounds_daily','rounds_life')
admin.site.register(Ladle,LadleAdmin)

class LadleUpdateRoomWiseAdmin(admin.ModelAdmin):
    list_display=('name','date','entry_time','room','exit_time','stop_points','first_time','entry_room','turn_overtime','turns')
admin.site.register(LadleUpdateRoomWise,LadleUpdateRoomWiseAdmin)

class EntriesAddedAdmin(admin.ModelAdmin):
    list_display=('name','date','count')
admin.site.register(EntriesAdded,EntriesAddedAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('name','comment')
admin.site.register(Comment,CommentAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display=('name','username','password')
admin.site.register(User,UserAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display=('name','username','password')
admin.site.register(Admin,AdminAdmin)
# Register your models here.

    
    
    