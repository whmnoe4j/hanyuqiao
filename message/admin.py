from django.contrib import admin
from django.db import models

from message.models import  Message, \
    MessageContent,Language, \
   MessageSubject,LocalMedia
class CustomModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self,request,obj=None):
        if not request.user.is_superuser and request.user.admin_type==2:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
class MediaInline(admin.StackedInline):
    model = LocalMedia

class ContentAdmin(admin.ModelAdmin):
    fields=('message','language','title','author','source')
    fields_l=('message','language','title','author','source','passed')
    list_display = ('title','passed')
    ordering=('id','passed')
    inlines=[MediaInline,]
    def get_fields(self, request, obj=None):
        if request.user.admin_type==1:
            return self.fields
        if request.user.admin_type==2:
            return self.fields_l
        form = self.get_form(request, obj, fields=None)
        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and request.user.admin_type==1:
            obj.passed=2
        obj.save()
    def get_readonly_fields(self,request,obj=None):
        if not request.user.is_superuser and request.user.admin_type==2:
            return ('message','title','language','author','source')
        return self.readonly_fields
admin.site.register(Language,CustomModelAdmin)
admin.site.register(MessageSubject,CustomModelAdmin)
admin.site.register(Message,CustomModelAdmin)
admin.site.register(MessageContent,ContentAdmin)
#admin.site.register(LocalMedia,CustomModelAdmin)

