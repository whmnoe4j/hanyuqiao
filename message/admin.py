from django.contrib import admin
from message.models import  Message, \
    MessageContent,Language, \
   MessageSubject, LocalMedia,RemoteMedia
class MessageAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Language)
admin.site.register(MessageSubject)
admin.site.register(Message,MessageAdmin)
admin.site.register(MessageContent,MessageAdmin)

