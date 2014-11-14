import requests
import json
baseurl='http://121.40.211.134'
def createtoken():
    s=requests.Session()
    url=baseurl+'/createtoken'
    data={'phone':'13482542201',}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def reg():
    s=requests.Session()
    url=baseurl+'/reg'
    data={'phone':'453479002','password':'1','token':'1','abroad':0}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def login():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'453479002@qq.com','password':'123'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
def if_introduction_exist():
    s=requests.Session()
    url=baseurl+'/if_introduction_exist/1.0.1'
    r=s.post(url)
    print r.status_code
    print r.content

def newest_introduction():
    s=requests.Session()
    url=baseurl+'/newest_introduction'
    r=s.post(url)
    print r.status_code
    print r.content
def if_update_introduction():
    s=requests.Session()
    url=baseurl+'/if_update_introduction'
    data={'pic':'InfoIm/E2449D7D-96CC-4C9D-8ED0-A88F1B3B9129.png','id':3}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
if_update_introduction()
def newest_version():
    s=requests.Session()
    url=baseurl+'/newest_version'
    r=s.post(url)
    print r.status_code
    print r.content

def get_language_list():
    s=requests.Session()
    url=baseurl+'/get_language_list'
    r=s.post(url)
    print r.status_code
    print r.content

def set_language():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/set_language'
    data={'languageid':'1'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
def translate():
    s=requests.Session()
    url=baseurl+'/translate/1/1'
    r=s.post(url)
    print r.status_code
    print r.content
def get_messages():
    s=requests.Session()
    url=baseurl+'/get_messages'
    data={'id':0,'start':0,'count':6}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
#get_messages()
def get_message():
    s=requests.Session()
    url=baseurl+'/get_message/1'

    r=s.post(url)
    print r.status_code
    print r.content
def set_favorite():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/set_favorite'
    data={'messageid':'1'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
def get_favorites():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/get_favorites'
    r=s.post(url)
    print r.status_code
    print r.content
def get_competitions():
    s=requests.Session()
    url=baseurl+'/get_competitions'
    r=s.post(url)
    print r.status_code
    print r.content

def get_competitionSubjects():
    s=requests.Session()
    url=baseurl+'/get_competitionSubjects/1'
    r=s.post(url)
    print r.status_code
    print r.content
#get_competitionSubjects()
def get_competition():
    s=requests.Session()
    url=baseurl+'/get_competition/1'
    r=s.post(url)
    print r.status_code
    print r.content

def get_players():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'hanyuqiao','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/get_players/5/1/1'
    r=s.post(url)
    print r.status_code
    print r.content
#get_players()
def search_players():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'hanyuqiao','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/search_players/1/1/1'
    data={'query':'1'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def vote():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'hanyuqiao','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/vote'
    data={'playerid':2}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def get_user():
    s=requests.Session()
    url=baseurl+'/get_user/1'

    r=s.post(url)

    print r.status_code
    print r.content
def modify_password():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'453479002@qq.com','password':'123'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
    url=baseurl+'/modify_password'
    data={'oldpassword':'123','newpassword':'1234'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
def update_user_info():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'hungerr','password':'1234'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
    url=baseurl+'/update_user_info'
    data={'desc':'1111','password':'1','gender':1,'abroad':'0','birthday':'1988-09-09','languageid':2}
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def if_cellphones_exist():
    s=requests.Session()
    url=baseurl+'/if_cellphones_exist'
    data={'cellphones':['xuefeihan','hungerr','hungerrr','hanyuqiao']}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def changepoint():
    s=requests.Session()
    url=baseurl+'/changepoint'
    data={'phoneoremail':'xuefeihan','point':'-10'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

