from django.contrib import admin

from appuser.models import MyUser,MyUserToken,Notification,ExtraNotification
class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['cellphone','cname','email','ename']
    filter_horizontal = ('friends','favorites',)
admin.site.register(MyUser,MyUserAdmin)
admin.site.register(MyUserToken)
