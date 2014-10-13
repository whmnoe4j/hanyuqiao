# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404
from django.db.models import Q, Min
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from hanyuqiao.models import Version,IntroductionImage
from message.models import MessageSubject, Message, MessageContent,Language
from appuser.models import MyUser,MyUserToken,Notification, ExtraNotification
from competition.models import Competition, Player
import json
import random
import datetime
from django.core.files.base import ContentFile

class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
           return None

        return (user, None)

def default_json_dump(obj):

    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d:%H:%M:%S')


def if_introduction_exist(request, version):
    return HttpResponse(
        json.dumps(
            Version.objects.filter(version=version).exists()),
        content_type="text/json")


@require_http_methods(["POST"])
def newest_version(request):
    return HttpResponse(
        Version.objects.order_by('-version')[0].version,
        content_type="text/json")


class Reg(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        try:
            data=json.loads(request.body)
        except:
            return Response({'success':False,'err_msg':'empty data'})
        abroad=data.get('abroad','')
        phone=data.get('phone','').strip()
        email=data.get('email','').strip()
        pw=data.get('password','').strip()
        token=data.get('token','').strip()
        if abroad=='0' or abroad==0: 
            try:
                usertoken=MyUserToken.objects.get(phone=phone)
                if usertoken.token==token:               
                    if phone and pw:
                        if MyUser.objects.filter(cellphone=phone).exists():
                            data={'success':False,'err_msg':'phone number was used'}
                        else:
                            user=MyUser.objects.create_user(cellphone=phone,password=pw)
                            user.abroad=0
                            user.save()
                            user=authenticate(cellphone=phone,password=pw)
                            login(request,user)
                            data={'success':True,'phone':phone}
                    else:
                        data={'success':False,'err_msg':'empty password'}
                else:
                    data={'success':False,'err_msg':u'2'}
         
            except:
                data={'success':False,'err_msg':u'wrong'}
        else:          
            if email and pw:
                if MyUser.objects.filter(email=email).exists():
                    data={'success':False,'err_msg':'email was used'}
                else:
                    user=MyUser.objects.create_user(cellphone=email,password=pw)
                    user.abroad=1
                    user.email=email
                    user.save()
                    user=authenticate(cellphone=email,password=pw)
                    login(request,user)
                    data={'success':True,'email':email}
            else:
                 data={'success':False,'err_msg':'empty password or email'}
        return Response(data)
                
class Login(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        try:
             body=json.loads(request.body)
        except:
            return Response({'success':False,'err_msg':'empty data'})
        phone=body.get('phoneoremail','').strip()
        pw=body.get('password','').strip()
        if phone and pw:
            user=authenticate(cellphone=phone,password=pw)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    data={'success':True,'phoneoremail':phone}
                else:
                    data={'success':False,'err_msg':'user is disabled'}
            elif MyUser.objects.filter(phoneNumber=phone).exists():
                data={'success':False,'err_msg':'wrong password'}
            else:
                data={'success':False,'err_msg':'phone number not register'}
        else:
            data={'success':False,'err_msg':'empty phone or password'}
        return Response(data)


@require_http_methods(["GET"])
def get_language_list(request):
    r = Language.objects.values('id', 'name')
    return HttpResponse(
        json.dumps(list(r)),
        content_type="text/json")



@require_http_methods(["POST"])
def set_language(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user

    if 'languageid' not in data:
        errormsg = u'没有传递languageid'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    else:
        languageid = data['languageid']

    try:
        language = Language.objects.get(id=int(languageid))
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    if user.is_authenticated():
        user.language = language
        user.save()
    else:
        return HttpResponse(json.dumps('未登录'), content_type='text/json')

    return HttpResponse(json.dumps(True), content_type='text/json')


@require_http_methods(["POST"])
def translate(request, messageid, languageid):
    try:
        language = Language.objects.get(id=int(languageid))
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    try:
        message = Message.objects.get(id=messageid)
    except Message.DoesNotExist:
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')

    try:
        messagecontent = message.messagecontent_set.get(language=language)
    except:
        errormsg = u'资讯没有此类语言'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')

    return HttpResponse(json.dumps({'title': messagecontent.title,
                                    'text': messagecontent.text}),
                        content_type='text/json')


@require_http_methods(["POST",'GET'])
def get_subjects(request):
    subjects = MessageSubject.objects.all().values('id','title')
    subjects = list(subjects)
    return HttpResponse(json.dumps(subjects), content_type='text/json')



@require_http_methods(["POST"])
def get_messages(request):
    data = json.loads(request.body)
    user = request.user
    language = user.language
    properties = data.get('properties', [
           "language", "title", "author",
          "source", "admin", "passed", "text", "postdate",
    "medias","messageid"])

    subject = data.get('subject')
    start = data.get('start', 0)
    count = data.get('count', 10)
    if subject:
        try:
            ms = MessageSubject.objects.get(title=subject)
        except MessageSubject.DoesNotExist:
            errormsg = u'主题不存在'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')
        else:
            messages = ms.message_set.all()[start:start+count]
    else:
        messages = Message.objects.all()[start:start+count]

    messagecontents = []
    for m in messages:
        mc_set = m.messagecontent_set
        if mc_set.count() <= 0:
            continue
        the_mc = None
        mc = mc_set.filter(language=language)
        if mc.count() <= 0:
            mc = m.messagecontent_set.annotate(
                min_index=Min('language__index'))
        the_mc = mc[0]
        values = dict([(e,getattr(the_mc, e)) for e in properties])
        messagecontents.append(values)

    messagecontents.sort(key=lambda e: e['postdate'])
    return HttpResponse(json.dumps(messagecontents, default=default_json_dump),
                        mimetype='text/json')
class GetMessages(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return MessageSubject.objects.get(pk=pk)
        except MessageSubject.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
        except:
            raise Http404
        user = request.user
        if user.is_authenticated and user.language:
            language = user.language
        else:
            language=Language.objects.order_by('index')[0]
        subject = int(data.get('id',0))
        start = int(data.get('start', 0))
        count = int(data.get('count', 8))
        if subject==0:
            messages = Message.objects.order_by('-postdate')[start:start+count]
        else:
            ms=self.get_object(subject)
            messages = ms.message_set.order_by('-postdate')[start:start+count]
        ms=[]
        for m in messages:
            if m.messagecontent_set.filter(language=language).exists():
                ms.append(m.messagecontent_set.get(language=language))
            else:
                ms.append(m.messagecontent_set.order_by('language__index')[0])
        data=[]
        for m in ms:
            data.append({'id':m.id,'title':m.title,'text':m.text})
        return Response(data)


@require_http_methods(["POST"])
def get_message(request, messageid):
    mc = MessageContent.objects.filter(id=int(messageid))
    if not mc.exists():
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    data=list(mc.values())
    data[0]['pubDate']=data[0]['pubDate'].strftime('%Y-%m-%d:%H:%M:%S')
    data[0]['postdate']=data[0]['postdate'].strftime('%Y-%m-%d:%H:%M:%S')
    print data
    return HttpResponse(json.dumps(data),content_type='text/json')



@require_http_methods(["POST"])
def set_favorite(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user
    messageid = data.get('messageid', -1)
    try:
        message = Message.objects.get(id=int(messageid))
    except Message.DoesNotExist:
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    if user.is_authenticated:
        user.favorites.add(message)
        user.save()
        return HttpResponse(json.dumps(True), content_type='text/json')
    else:
        return HttpResponse(json.dumps('not login'), content_type='text/json')
        

@require_http_methods(["POST"])
def get_favorites(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps('not login'),
                        content_type='text/json')        
    user = request.user
    language = user.language
    r = []
    for m in user.favorites.all():
        r.extend(
            list(
                m.messagecontent_set.filter(
                    language=language).values(
                    'id',
                    'title')))

    return HttpResponse(json.dumps(r),
                        content_type='text/json')



@require_http_methods(["POST"])
def get_competitionSubjects(request):
    # since sqlite does not support distinct
    subjects = Competition.objects.all().values_list('subject')
    subjects = list(set([e[0] for e in subjects]))
    return HttpResponse(json.dumps(subjects),
                        content_type='text/json')



@require_http_methods(["POST"])
def get_competitions(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    competitions = Competition.objects
    if 'subject' in data:
        competitions = competitions.filter(subject=data['subject'])
    if 'category' in data:
        competitions = competitions.filter(category=data['category'])
    else:
        competitions = competitions.all()
    competitions = list(competitions.values())
    return HttpResponse(json.dumps(competitions, default=default_json_dump),
                        mimetype='text/json')

class GetPlayers(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            raise Http404
    def post(self, request,cpk,apk,page, format=None):
        cpk=int(cpk)
        apk=int(apk)
        page=int(page)
        c=self.get_object(cpk)
        players= Player.objects.filter(competition=c,isout=False)
        canvote=True
        votemanid=None
        if request.user.is_authenticated: 
            for p in players:
                if p.whovotes.filter(id=request.user.id).exists():
                    canvote=False
                    votemanid=p.id
                    break
        start=(page-1)*10
        end=start+10
        players= Player.objects.filter(competition=c,area=apk).order_by('sn').values()[start:end]
        data={'canvote':canvote,'votedplayerid':votemanid,'players':players}
        return Response(data)
        
def search_players(request):
    try:
        data = json.loads(request.body)
    except:
        errormsg = u'参数传递错误'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    q = Q()
    for k, v in data.items():
        if k in ['userid', 'token']:
            continue
        if k in ['desc', 'interist', ]:
            k = 'playerinfo__'+k+'__icontains'
        q = q & eval('Q(%s="%s")' % (k, v))

    players = Player.objects.filter(q)
    players = list(players.values())
    for p in players:
        player = Player.objects.get(sn=p['sn'])
        p['whovotes']=list(player.whovotes.all().values())
        p['info']=list(player.playerinfo_set.values())
    return HttpResponse(json.dumps(players, default=default_json_dump),
                        mimetype='text/json')



@require_http_methods(["POST"])
def vote(request):
    data = request.data
    user = request.user

    if 'sn' not in data:
        errormsg = u'没有传递sn'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    else:
        sn = data['sn']
    try:
        player = Player.objects.get(sn=sn)
    except Player.DoesNotExist:
        errormsg = u'选手不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    competition = player.competition
    whovotes = list(competition.player_set.filter(isout=False).values_list("whovotes"))
    whovotes = [e[0] for e in whovotes if e[0]]
    if user.id in whovotes:
        errormsg = u'已经投过票'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    player.whovotes.add(user)
    player.save()

    return HttpResponse(json.dumps(True),
                        mimetype='text/json')
class Vote(APIView):
    authentication_classes = (UnsafeSessionAuthentication,BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Player.objects.get(id=pk)
        except Player.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
        except:
            raise Http404
        pk=data.get('playerid','')
        if pk:
            player=self.get_object(int(pk))
        else:
            return Response('empty player index')
        
        players=player.competition.player_set.filter(isout=False)
        for p in players:
            if p.whovotes.filter(id=request.user.id).exists():
                return Response('can not vote because have voted')
        player.whovotes.add(request.user)
        player.votenum+=1
        player.save()
        return Response(True)

@require_http_methods(["POST"])
def get_user(request, userid):
    user = MyUser.objects.filter(id=userid)
    if user.count() == 1:
        user = list(user.values())[0]
        return HttpResponse(json.dumps(user, default=default_json_dump),
                            mimetype='text/json')
    else:
        errormsg = u'用户不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')






@require_http_methods(["POST"])
def if_cellphones_exist(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    cellphones = data.get('cellphones', [])
    users = MyUser.objects.filter(cellphone__in=cellphones).values()
    return HttpResponse(json.dumps(list(users), default=default_json_dump),
                        mimetype='text/json')





@require_http_methods(["POST"])
def modify_password(request):
    require_fields = ['cellphone', 'oldpassword', 'newpassword']
    for field in require_fields:
        if field not in request.POST:
            errormsg = u'没有传递%s' % field
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')
    try:
        myuser = MyUser.objects.get(cellphone=request.POST['cellphone'])
    except MyUser.DoesNotExist:
        errormsg = u'用户名密码不匹配'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    if myuser.user.check_password(request.POST['oldpassword']) is False:
        errormsg = u'用户名密码不匹配'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    try:
        myuser.user.set_password(request.POST['newpassword'])
        myuser.user.save()
        myuser.save()
    except Exception as e:
        errormsg = str(e)
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    return HttpResponse(json.dumps(True),
                        mimetype='text/json')



@require_http_methods(["POST"])
def update_user_info(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user
    try:
        for k, v in data.items():
            if k in ('userid', 'token', 'password'):
                continue
            setattr(user, k, v)
    except Exception as e:
        errormsg = str(e)
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    user.save()
    return HttpResponse(json.dumps(True),
                        mimetype='text/json')



@require_http_methods(["POST"])
def get_friends_list(request):
    user = request.user
    friends = list(user.friends.values())
    return HttpResponse(
        json.dumps(friends, default=default_json_dump),
        mimetype='text/json')



def get_notifications(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user
    not_read = data.get('not_read', False)
    cnt = data.get('cnt', 20)

    if not_read:
        extra_notifications = user.extranotification_set.filter(
            hasread=False)[
            : cnt]
    else:
        extra_notifications = user.extranotification_set.all()[:cnt]
    notifications = [(e.id, e.notification.title, e.notification.postdate)
                     for e in extra_notifications]
    notifications.sort(key=lambda x: x[-1])

    return HttpResponse(json.dumps(notifications, default=default_json_dump),
                        mimetype='text/json')



def get_notification(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    # notificationid is really extra_notificationid
    if 'notificationid' not in data:
        errormsg = u'没有传递notificationid'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    else:
        notificationid = data['notificationid']

    try:
        extra_notification = ExtraNotification.objects.get(id=notificationid)
    except ExtraNotification.DoesNotExist:
        errormsg = u'没有此消息'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    extra_notification.hasread = True
    extra_notification.save()

    r = (extra_notification.notification.title,
         extra_notification.notification.text)

    return HttpResponse(json.dumps(r), mimetype='text/json')



@require_http_methods(["POST"])
def invite(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user
    if 'target_cellphone' not in data:
        errormsg = u'没有传递target_cellphone'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    target_cellphone = data['target_cellphone']
    try:
        target_user = MyUser.objects.get(cellphone=target_cellphone)
    except MyUser.DoesNotExist:
        errormsg = u'没有目标用户'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    if target_user in user.friends.all():
        errormsg = u'对方已在里的好友列表'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    notification = Notification(
        title=u'%s邀请你加为他/她的好友' %
        user.cellphone,
        text=u'')
    notification.save()

    en = ExtraNotification(notification=notification, user=target_user)
    en.save()

    return HttpResponse(json.dumps(True), mimetype='text/json')



def pass_invite(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user

    if 'target_cellphone' not in data:
        errormsg = u'没有传递target_cellphone'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    target_cellphone = data['target_cellphone']
    try:
        target_user = MyUser.objects.get(cellphone=target_cellphone)
    except MyUser.DoesNotExist:
        errormsg = u'没有目标用户'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    user.friends.add(target_user)
    user.save()

    target_user.friends.add(user)
    target_user.save()

    notification = Notification(title=u'%s通过你的邀请' % user.cellphone, text=u'')
    notification.save()

    en = ExtraNotification(notification=notification, user=target_user)
    en.save()

    return HttpResponse(json.dumps(True), mimetype='text/json')



def deny_invite(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    user = request.user

    if 'target_cellphone' not in data:
        errormsg = u'没有传递target_cellphone'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    target_cellphone = data['target_cellphone']
    try:
        target_user = MyUser.objects.get(cellphone=target_cellphone)
    except MyUser.DoesNotExist:
        errormsg = u'没有目标用户'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    notification = Notification(title=u'%s拒绝你的邀请' % user.cellphone, text=u'')
    notification.save()

    en = ExtraNotification(notification=notification, user=target_user)
    en.save()

    return HttpResponse(json.dumps(True), mimetype='text/json')
