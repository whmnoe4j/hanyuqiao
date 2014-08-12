hanyuqiao
=========

汉语桥
api.py修改：
@require_http_methods(["GET"])  -----------    @require_http_methods(["GET",'OPTIONS'])
@require_http_methods(["POST"])  -----------   @require_http_methods(["POST",'OPTIONS'])

def get_user_by_uid_or_create(request, uid):
    user = User(username=cellphone, password='default') ------ user = User.objects.create_user(username=cellphone, password='default')

def get_messages(request):
    ms = MessageSubject.get(subject=subject)  ------   ms = MessageSubject.objects.get(title=subject)

def get_favorites(request):
    r.append   -------    r.extend

def if_cellphone_exist(request, cellphone):  去掉了@token_required装饰器

def invite(request):   加了个对方是否已在好友列表的判断

测试在test.py中
python manage.py test hanyuqiao
