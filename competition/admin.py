from django.contrib import admin
from competition.models import  Competition, Player

class CustomModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self,request,obj=None):
        if not request.user.is_superuser and request.user.admin_type==2:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
class PlayerAdmin(CustomModelAdmin):
    search_fields = ['cname', 'ename']
    filter_horizontal = ('whovotes',)
admin.site.register(Competition,CustomModelAdmin)
admin.site.register(Player,PlayerAdmin)

