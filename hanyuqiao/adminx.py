#!encoding=utf-8
from hanyuqiao.models import Version, IntroductionImage, Message, \
    MessageContent, Competition, Player, PlayerInfo, MyUser,Language, \
    Notification, ExtraNotification,MessageSubject
import xadmin

class ExtraNotificationInline(object):
    model = ExtraNotification
    extra = 0
    style = 'accordion'
class MyUserAdmin(object):
    inlines = [ExtraNotificationInline]


class IntroductionImageInline(object):
    model = IntroductionImage
    extra = 1
    style = 'accordion'
class VersionAdmin(object):
    inlines = [IntroductionImageInline]


class MessageContentInline(object):
    model = MessageContent
    extra = 1
    style = 'accordion'
class MessageAdmin(object):
    inlines = [MessageContentInline]

class MessageInline(object):
    model = Message
    extra = 0
class MessageSubjectAdmin(object):
    inlines = [MessageInline]


class PlayerInfoInline(object):
    model = PlayerInfo
    extra = 1
class PlayerAdmin(object):
    inlines = [PlayerInfoInline]

xadmin.site.register(Language)
xadmin.site.register(MyUser,MyUserAdmin)
xadmin.site.register(Version,VersionAdmin)
xadmin.site.register(IntroductionImage)
xadmin.site.register(MessageSubject,MessageSubjectAdmin)
xadmin.site.register(Message,MessageAdmin)
xadmin.site.register(MessageContent)
xadmin.site.register(Competition)
xadmin.site.register(Player, PlayerAdmin)
xadmin.site.register(Notification)
xadmin.site.register(ExtraNotification)
