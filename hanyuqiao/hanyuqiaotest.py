import requests
import json
s=requests.Session()
url='http://127.0.0.1:8000/login'
data={'phoneoremail':'xuefeihan','password':'111','token':'111','abroad':'0'}
data=json.dumps(data)
r=s.post(url,data=data)
print r.status_code
print r.content
data={'playerid':1}
data=json.dumps(data)
url='http://127.0.0.1:8000/vote'
r=s.post(url,data=data)
print r.status_code
print r.content
