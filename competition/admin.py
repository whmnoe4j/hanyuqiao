from django.contrib import admin
from competition.models import  Competition, Player

class CustomModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self,request,obj=None):
        if not request.user.is_superuser and request.user.admin_type==2:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
class PlayerAdmin(CustomModelAdmin):
    search_fields = ('cname', 'ename','country','ci','competition__title','competition__subject',)
    filter_horizontal = ('whovotes',)
    list_display = ('cname', 'ename','country','ci','competition')
    list_filter = ('cname', 'ename','country','ci','competition')
admin.site.register(Competition,CustomModelAdmin)
admin.site.register(Player,PlayerAdmin)

