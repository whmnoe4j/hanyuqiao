# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q, Min
from django.views.decorators.http import require_http_methods
from hanyuqiao.models import Version, Notification, ExtraNotification,\
    MessageSubject, Message, MessageContent, Competition, \
    Player, MyUser, Language
import json
import random
import datetime


def token_required(func):
    def inner(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            errormsg = u'参数传递错误'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')

        if 'userid' not in data:
            errormsg = u'没有传递userid'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')
        else:
            userid = data['userid']

        if 'token' not in data:
            errormsg = u'没有传递token'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')

        try:
            user = MyUser.objects.get(id=userid)
        except MyUser.DoesNotExist:
            errormsg = u'用户不存在'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')

        if data['token'] != user.token:
            errormsg = u'token错误'
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')
        request.data = data
        request.user = user
        return func(request, *args, **kwargs)
    return inner


def default_json_dump(obj):

    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()


def if_introduction_exist(request, version):
    return HttpResponse(
        json.dumps(
            Version.objects.filter(version=version).exists()),
        mimetype="text/json")


@require_http_methods(["GET"])
def newest_version(request):
    return HttpResponse(
        Version.objects.order_by('-version')[0].version,
        mimetype="text/json")


@require_http_methods(["POST", 'OPTIONS'])
def get_user_by_uid_or_create(request, uid):
    try:
        data = json.loads(request.body)
    except:
        errormsg = u'参数传递错误'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    cellphone = data.get('cellphone','')
    try:
        myuser = MyUser.objects.get(uid=uid)
        userid = myuser.id
        token = myuser.token
        return HttpResponse(
            json.dumps({'token': token, 'userid': userid, 'created': False}),
            mimetype="text/json")
    except MyUser.DoesNotExist:
        user = User.objects.create_user(username=uid, password='default')
        user.save()
        myuser = MyUser(user=user, uid=uid, cellphone=cellphone)
        token = str(random.random())[2:]+str(random.random())[2:]
        myuser.token = token
        myuser.save()
        userid = myuser.id
        return HttpResponse(
            json.dumps({'token': token, 'userid': userid, 'created': True}),
            mimetype="text/json")


@require_http_methods(["GET"])
def get_language_list(request):
    r = Language.objects.values('id', 'name')
    return HttpResponse(
        json.dumps(list(r)),
        mimetype="text/json")


@token_required
@require_http_methods(["POST", 'OPTIONS'])
def set_language(request):
    data = request.data
    user = request.user

    if 'languageid' not in data:
        errormsg = u'没有传递languageid'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    else:
        languageid = data['languageid']

    try:
        language = Language.objects.get(id=languageid)
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    user.language = language
    user.save()

    return HttpResponse(json.dumps(True), mimetype='text/json')


@require_http_methods(["GET"])
def translate(request, messageid, languageid):
    try:
        language = Language.objects.get(id=languageid)
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    try:
        message = Message.objects.get(id=messageid)
    except Message.DoesNotExist:
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    try:
        messagecontent = message.messagecontent_set.get(language=language)
    except:
        errormsg = u'资讯没有此类语言'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    return HttpResponse(json.dumps({'title': messagecontent.title,
                                    'text': messagecontent.text}),
                        mimetype='text/json')


@token_required
@require_http_methods(["GET"])
def get_subjects(request):
    subjects = MessageSubject.objects.all().value_lists('title')
    return HttpResponse(json.dumps(subjects), mimetype='text/json')


@token_required
@require_http_methods(["GET", 'OPTIONS'])
def get_messages(request):
    data = request.data
    user = request.user
    language = user.language
    subject = data.get('subject')
    start = data.get('start')
    count = data.get('count')
    if subject:
        print 'subject: '+subject
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
        mc = m.messagecontent_set.filter(language=language)
        if mc.count() > 0:
            messagecontents.extend(list(mc.values()))
        else:
            _ = m.messagecontent_set.annotate(
                min_index=Min('language__index')).values()
            messagecontents.extend(_[:1])

    messagecontents.sort(key=lambda e: e['postdate'])
    return HttpResponse(json.dumps(messagecontents, default=default_json_dump),
                        mimetype='text/json')


@require_http_methods(["GET"])
def get_message(request, messageid):
    mc = MessageContent.objects.filter(id=messageid)
    if not mc.exists():
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    return HttpResponse(
        json.dumps(
            list(
                mc.values()),
            default=default_json_dump),
        mimetype='text/json')


@token_required
@require_http_methods(["POST", 'OPTIONS'])
def set_favorite(request):
    data = request.data
    user = request.user

    messageid = data.get('messageid', -1)
    try:
        message = Message.objects.get(id=messageid)
    except Message.DoesNotExist:
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    user.favorites.add(message)

    return HttpResponse(json.dumps(True), mimetype='text/json')


@token_required
@require_http_methods(["GET", 'OPTIONS'])
def get_favorites(request):
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
                        mimetype='text/json')


@token_required
@require_http_methods(["GET"])
def get_competitionSubjects(request):
    #since sqlite does not support distinct
    subjects=Competition.objects.all().valuse_list('subject')
    subjects=[e[0] for e in subjects]
    return HttpResponse(json.dumps(subjects),
                        mimetype='text/json')

@token_required
@require_http_methods(["GET"])
def get_competitions(request):
    data = request.data
    competitions = Competition.objects
    if 'subject' in data:
        competitions=competitions.filter(subject=data['subjects'])
    if 'category' in data:
        competitions=competitions.filter(category=data['category'])
    else:
        competitions=competitions.all()
    competitions = list(competitions.values())
    return HttpResponse(json.dumps(competitions, default=default_json_dump),
                        mimetype='text/json')


@require_http_methods(["GET"])
def get_players(request, competitionid):
    players = Player.objects.filter(competition=competitionid).values()
    players = list(players)
    return HttpResponse(json.dumps(players, default=default_json_dump),
                        mimetype='text/json')


@token_required
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
    print json.dumps(players, default=default_json_dump)
    return HttpResponse(json.dumps(players, default=default_json_dump),
                        mimetype='text/json')


@token_required
@require_http_methods(["POST", 'OPTIONS'])
def vote(request):
    data = request.data
    user = request.user

    if 'playerid' not in data:
        errormsg = u'没有传递playerid'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')
    else:
        playerid = data['playerid']
    try:
        player = Player.objects.get(id=playerid)
    except Player.DoesNotExist:
        errormsg = u'选手不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    if user in player.whovotes.all():
        errormsg = u'已经投过票'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    player.votes = player.votes + 1
    player.whovotes.add(user)
    player.save()

    return HttpResponse(json.dumps(True),
                        mimetype='text/json')


@require_http_methods(["GET"])
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
def register(request):
    require_fields = ['cellphone', 'password']
    for field in require_fields:
        if field not in request.POST:
            errormsg = u'没有传递%s' % field
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')

    try:
        user = User(username=request.POST['cellphone'])
        user.set_password(request.POST['password'])
        user.save()

        myuser = MyUser(user=user, cellphone=request.POST['cellphone'])
        for k, v in request.POST.items():
            if k in ['password', 'cellphone']:
                continue
            setattr(myuser, k, v)
        myuser.save()
    except Exception as e:
        errormsg = str(e)
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    return HttpResponse(json.dumps(True),
                        mimetype='text/json')


@require_http_methods(["GET"])
def if_cellphone_exist(request, cellphone):
    exist = MyUser.objects.filter(cellphone=cellphone).exists()
    return HttpResponse(json.dumps(exist),
                        mimetype='text/json')


@require_http_methods(["POST"])
def login(request):
    require_fields = ['cellphone', 'password']
    for field in require_fields:
        if field not in request.POST:
            errormsg = u'没有传递%s' % field
            return HttpResponse(json.dumps({'errormsg': errormsg}),
                                mimetype='text/json')
    cellphone = request.POST["cellphone"]
    password = request.POST["password"]

    try:
        myuser = MyUser.objects.get(cellphone=cellphone)
    except MyUser.DoesNotExist:
        errormsg = u'用户名密码不匹配'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    if myuser.user.check_password(password) is False:
        errormsg = u'用户名密码不匹配'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            mimetype='text/json')

    myuser.token = str(random.random())[2:]+str(random.random())[2:]
    myuser.save()

    return HttpResponse(
        json.dumps({'token': myuser.token, 'userid': myuser.id}),
        mimetype="text/json")


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


@token_required
@require_http_methods(["POST", 'OPTIONS'])
def update_user_info(request):
    data = request.data
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


@token_required
@require_http_methods(["GET"])
def get_friends_list(request):
    user = request.user
    friends = list(user.friends.values())
    return HttpResponse(
        json.dumps(friends, default=default_json_dump),
        mimetype='text/json')


@token_required
def get_notifications(request):
    data = request.data
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


@token_required
def get_notification(request):
    data = request.data
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


@token_required
@require_http_methods(["POST", 'OPTIONS'])
def invite(request):
    data = request.data
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


@token_required
def pass_invite(request):
    data = request.data
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


@token_required
def deny_invite(request):
    data = request.data
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
