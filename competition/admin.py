from django.contrib import admin
from competition.models import  Competition, Player, PlayerInfo
class PlayerInfoInline(admin.ModelAdmin):
    model = PlayerInfo
    extra = 1
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ['cname', 'ename']
    filter_horizontal = ('whovotes',)
admin.site.register(Competition)
admin.site.register(Player,PlayerAdmin)
admin.site.register(PlayerInfo)
