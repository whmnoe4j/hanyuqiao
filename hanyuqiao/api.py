# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404
from django.db.models import Q, Min
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext   
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from django.contrib.admin.models import LogEntry
from hanyuqiao.models import Version,IntroductionImage,Hanyuqiao
from message.models import MessageSubject, Message, MessageContent,Language
from appuser.models import MyUser,MyUserToken
from competition.models import Competition, Player
import json
import random
import datetime
from django.core.files.base import ContentFile
import requests

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


def newest_introduction(request):
    i=IntroductionImage.objects.last()
    if i:
        data={'pic':i.pic.name,'messageid':i.message.id}
    else:
        data=False
    return HttpResponse(
        json.dumps(data),
        content_type="text/json")
def abouthanyuqiao(request):
    i=Hanyuqiao.objects.last()
    if i:
        data={'text':i.desc}
    else:
        data=False
    return HttpResponse(
        json.dumps(data),
        content_type="text/json")

@require_http_methods(["POST"])
def newest_version(request):
    return HttpResponse(
        Version.objects.order_by('-version')[0].version,
        content_type="text/json")
class CreateToken(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def send_token(self,token,phone):
        url='http://www.810086.com.cn/jk.aspx'
        content='【汉语桥】您的验证码是'+token
        data={'zh':'zhoulang11','mm':'123456789','hm':phone,'nr':content,'sms_type':42}
        r=requests.post(url,data=data)
        return r.content
    def post(self, request, format=None):
        try:
            data=json.loads(request.body)
        except:
            return Response({'success':False,'err_msg':'empty data'})
        phone=data.get('phone','')
        phone=str(phone)
        if phone:
            user,created=MyUserToken.objects.get_or_create(phone=phone)
            token=random.randint(100000,999999)
            user.token=str(token)
            user.save()
            result=self.send_token(str(token),phone)
            if result.startswith('0'):
                data={'success':True}
                return Response(data)
            else:
                data={'success':False,'err_code':result}
                return Response(data)
        else:
            data={'success':False,'err_msg':'empty phone','err_code':1004}
            return Response({'successw':False})

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
        phone=str(phone)
        email=data.get('email','').strip()
        pw=data.get('password','').strip()
        token=data.get('token','').strip()
        token=str(token)
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
                            data={'success':True,'phone':phone}
                    else:
                        data={'success':False,'err_msg':'empty password'}
                else:
                    data={'success':False,'err_msg':u'wrong token'}
         
            except:
                data={'success':False,'err_msg':u'token donot exists'}
        else:          
            if email and pw:
                if MyUser.objects.filter(email=email).exists():
                    data={'success':False,'err_msg':'email was used'}
                else:
                    user=MyUser.objects.create_user(cellphone=email,password=pw)
                    user.abroad=1
                    user.email=email
                    user.save()
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
                    data={'success':True,'phoneoremail':phone,'id':user.id}
                else:
                    data={'success':False,'err_msg':'user is disabled'}
            elif MyUser.objects.filter(cellphone=phone).exists():
                data={'success':False,'err_msg':'wrong password'}
            else:
                data={'success':False,'err_msg':'need reg'}
        else:
            data={'success':False,'err_msg':'empty phone or password'}
        return Response(data)


@require_http_methods(["GET",'POST'])
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
    if not user.is_authenticated():
        return HttpResponse(json.dumps({'errormsg': 'need login'}),
                            content_type='text/json')
    if 'languageid' not in data:
        errormsg = u'没有传递languageid'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    else:
        languageid = data['languageid']

    try:
        language = Language.objects.get(id=int(languageid))
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    
    user.language = language
    user.save()
    return HttpResponse(json.dumps(True), content_type='text/json')


@require_http_methods(["POST"])
def translate(request, messageid, languageid):
    try:
        language = Language.objects.get(id=int(languageid))
    except Language.DoesNotExist:
        errormsg = u'语言不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')

    try:
        message = Message.objects.get(id=int(messageid))
    except Message.DoesNotExist:
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')

    try:
        mc = message.messagecontent_set.get(language=language)
    except:
        errormsg = u'资讯没有此类语言'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    data={}
    data['id']=mc.message.id
    data['title']=mc.title
    data['author']=mc.author
    data['source']=mc.source
    data['languageid']=mc.language.id
    data['languagename']=mc.language.name
    data['date']=mc.postdate.strftime('%Y-%m-%d:%H:%M:%S')
    data['content']=list(mc.localmedia_set.order_by('id').values('mediatype','text','pictitle','mediafile','remotefile'))
    return HttpResponse(json.dumps(data),content_type='text/json')

@require_http_methods(["POST",'GET'])
def get_subjects(request):
    subjects = MessageSubject.objects.all().values('id','title')
    subjects = list(subjects)
    return HttpResponse(json.dumps(subjects), content_type='text/json')

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
        if user.is_authenticated() and user.language:
             language = user.language
        else:
            language=Language.objects.order_by('index')[0]
        subject = int(data.get('id',0))
        start = int(data.get('start', 0))
        count = int(data.get('count', 8))
        if subject==0:
            messages = Message.objects.filter(messagecontent__passed=3).order_by('-postdate')[start:start+count]
        else:
            ms=self.get_object(subject)
            messages = ms.message_set.filter(messagecontent__passed=3).order_by('-postdate')[start:start+count]
        ms=[]
        for m in messages:
            if m.messagecontent_set.filter(language=language,passed=3).exists():
                ms.append(m.messagecontent_set.get(language=language))
            else:
                ms.append(m.messagecontent_set.filter(passed=3).order_by('language__index')[0])
        data=[]
        for m in ms:
            md={'id':m.id,'date':m.postdate.strftime('%Y-%m-%d:%H:%M:%S'),'title':m.title,'text':m.localmedia_set.all()[0].text}
            for media in m.localmedia_set.all():
                if media.mediafile:
                    md['pic']=media.mediafile.name
                    break
            data.append(md)         
        return Response(data)


@require_http_methods(["POST",'GET'])
def get_message(request, messageid):
    mc = MessageContent.objects.filter(id=int(messageid))
    if not mc.exists():
        errormsg = u'资讯不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_type='text/json')
    mc=mc[0]
    data={}
    data['id']=mc.message.id
    data['title']=mc.title
    data['author']=mc.author
    data['source']=mc.source
    data['languageid']=mc.language.id
    data['languagename']=mc.language.name
    data['date']=mc.postdate.strftime('%Y-%m-%d:%H:%M:%S')
    data['content']=list(mc.localmedia_set.order_by('id').values('mediatype','text','pictitle','mediafile','remotefile'))
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
    if user.is_authenticated():
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
    subjects = Competition.objects.order_by('-pubDate','startdate').values('id','title','canvote')
    subjects = list(subjects)
    return HttpResponse(json.dumps(subjects),
                        content_type='text/json')



@require_http_methods(["POST"])
def get_competition(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    pk=data.get('id','')
    try:
        pk=int(pk) 
        competition = Competition.objects.get(id=pk)
    except:
        raise Http404
    data={}
    data['subject']=competition.subject
    if competition.pic:
        data['pic']=competition.pic.name
    data['startdate']=competition.startdate.strftime('%Y-%m-%d')
    data['enddate']=competition.enddate.strftime('%Y-%m-%d')
    return HttpResponse(json.dumps(data),
                       content_type='text/json')

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
        if request.user.is_authenticated(): 
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
class SearchPlayers(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request,cpk,apk,page, format=None):
        try:
            data = json.loads(request.body)
        except:
            errormsg = u'参数传递错误'
            return Response({'errormsg': errormsg})
        cpk=int(cpk)
        apk=int(apk)
        page=int(page)
        name=data.get('query','')
        start=(page-1)*10
        end=start+10
        players= Player.objects.filter(Q(cname__icontains=name) | Q(ename__icontains=name)| Q(desc__icontains=name)| Q(country__icontains=name),competition__id=cpk,area=apk).order_by('sn').values()[start:end]
        return Response(players)

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
                return Response({'sucess':False,'err':'can not vote because have voted'})
        if datetime.date.today()>player.competition.enddate:
            return Response({'sucess':False,'err':'vote is over'})
        player.whovotes.add(request.user)
        player.votenum+=1
        player.save()
        return Response({'sucess':True,'num':player.votenum})

@require_http_methods(["POST"])
def get_user(request, userid):
    user = MyUser.objects.filter(id=userid)
    if user.exists():
        user = list(user.values())[0]
        return HttpResponse(json.dumps(user, default=default_json_dump),
                           content_type='text/json')
    else:
        errormsg = u'用户不存在'
        return HttpResponse(json.dumps({'errormsg': errormsg}),
                            content_ype='text/json')

@require_http_methods(["POST"])
def if_cellphones_exist(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    cellphones = data.get('cellphones', [])
    phones=[]
    for cellphone in cellphones:
        if MyUser.objects.filter(cellphone=cellphone).exists():
            phones.append(cellphone)
    return HttpResponse(json.dumps(phones),
                        content_type='text/json')

class ModifyPassword(APIView):
    authentication_classes = (UnsafeSessionAuthentication,BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
        except:
            raise Http404
        old=data.get('oldpassword','')
        new=data.get('newpassword','')
        if not old or not new:
            return Response({'success':False,'err':'empty password'})
        if request.user.check_password(old) is False:
            return Response({'success':False,'err':'wrong password'})
        request.user.set_password(new)
        request.user.save()
        return Response({'success':True})

class UpdateUserData(APIView):
    authentication_classes = (UnsafeSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user=request.user       
        for attr in ['nick','cname','email','f_l','born_place','inte','country','university','city','desc','career']:
            if request.POST.get(attr,''):
                setattr(user,attr,request.POST.get(attr,''))
        for attr in ['gender','tel','abroad','zipcode','education','degree','religion','blood','star','zod']:
            if request.POST.get(attr,''):
                setattr(user,attr,int(request.POST.get(attr,'')))
        for attr in ['birthday','installdate']:
            if request.POST.get(attr,''):
                year=int(request.POST.get(attr,'')[:4])
                month=int(request.POST.get(attr,'')[5:7])
                day=int(request.POST.get(attr,'')[8:10])
                date=datetime.date(year,month,day)
                setattr(user,attr,date)
        languageid=request.POST.get('languageid','')
        if languageid:
            l=Language.objects.get(id=int(languageid))
            user.language=l
        img=request.FILES.get('head','')
        if img:
            if img.size<3000000:
                file_content = ContentFile(img.read()) 
                user.pic.save(img.name, file_content)
            else:
                data={'success':False,'err':'too big img'}
                return Response(data)
        user.save()
        datauser = MyUser.objects.filter(id=user.id)
        data=list(datauser.values())[0]
        return Response(data)

def history(request,page):
    start=100*(int(page)-1)
    end=start+100
    if request.user.is_admin:
        return render_to_response(  
        "admin/history.html",  
        {'action_list' : LogEntry.objects.all()[start:end]},  
        RequestContext(request, {}),  
    )
    else:
        raise Http404
@require_http_methods(["POST"])
def addpoint(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404
    phone=data.get('phoneoremail','')
    point=data.get('point',0)
    point=int(point)
    try:
        user = MyUser.objects.get(cellphone=phone)
    except:
        raise Http404 
    user.point+=point
    if user.point<0:
        return HttpResponse(json.dumps({'success':False,'err':'ponit < 0'}),
                        content_type='text/json')
    user.save()
    return HttpResponse(json.dumps({'success':True,'point':user.point}),
                        content_type='text/json')
