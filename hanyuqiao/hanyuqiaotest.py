import requests
import json
baseurl='http://121.40.211.134'
def login():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
login()
def if_introduction_exist():
    s=requests.Session()
    url=baseurl+'/if_introduction_exist/1.0.1'
    r=s.post(url)
    print r.status_code
    print r.content
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
    data={'id':1,'start':0,'end':8}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

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
def get_competitionSubjects():
    s=requests.Session()
    url=baseurl+'/get_competitionSubjects'
    r=s.post(url)
    print r.status_code
    print r.content
def get_competition():
    s=requests.Session()
    url=baseurl+'/get_competition'
    data={'id':1}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content
def get_players():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/get_players/1/1/1'
    r=s.post(url)
    print r.status_code
    print r.content

def search_players():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
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
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
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
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/modify_password'
    data={'oldpassword':'111','newpassword':'1'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    print r.status_code
    print r.content

def update_user_info():
    s=requests.Session()
    url=baseurl+'/login'
    data={'phoneoremail':'xuefeihan','password':'1','token':'111','abroad':'0'}
    data=json.dumps(data)
    r=s.post(url,data=data)
    url=baseurl+'/update_user_info'
    data={'desc':'1111','password':'1','gender':1,'abroad':'0'}
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

