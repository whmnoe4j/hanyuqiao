# -*- coding: utf-8 -*-
import requests
import json
import unittest

#print >> open('log.html','w'),r.text

host = '127.0.0.1'
port = 8000
u = 'http://%s:%s' % (host, port)


class mytest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_if_introduction_exist(self):
        version = '1.0'
        r = requests.get(
            '%s/if_introduction_exist/%s' %
            (u, version)).json()
        self.assertEqual(r, True)

        version = '1.01'
        r = requests.get(
            '%s/if_introduction_exist/%s' %
            (u, version)).json()
        self.assertEqual(r, False)

    def test_newest_version(self):
        r = requests.get('%s/newest_version' % u).text
        self.assertEqual(r, '1.0')

    def test_set_language(self):
        userid = 1000
        languageid = 1
        token = '12129403243'
        data = {'userid': userid, 'languageid': languageid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_language'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, {u'errormsg': u'用户不存在'})

        userid = 1
        languageid = 1
        token = '12129403243'
        data = {'userid': userid, 'languageid': languageid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_language'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, {'errormsg': u'token错误'})

        userid = 1
        languageid = 10000
        token = '123456'
        data = {'userid': userid, 'languageid': languageid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_language'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, {'errormsg': u'语言不存在'})

        userid = 1
        languageid = 1
        token = '123456'
        data = {'userid': userid, 'languageid': languageid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_language'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, True)

    def test_translate(self):
        messageid = 1
        languageid = 1
        r = requests.get(
            '%s/%s/%s/%s' %
            (u, 'translate', messageid, languageid))

        self.assertEqual(r.json(), {'errormsg': u'资讯没有此类语言'})

        messageid = 1
        languageid = 2
        r = requests.get(
            '%s/%s/%s/%s' %
            (u, 'translate', messageid, languageid))

        self.assertEqual(r.json(), {'title': u'资讯1', 'text': u'资讯1内容'})

    def test_get_messages(self):
        #languageid = 1
        userid = 1
        token = '123456'
        data={'userid':userid,'token':token}
        r = requests.get('%s/%s' % (u, 'get_messages'),data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_get_subjects(self):
        userid = 1
        token = '123456'
        data = {'userid':userid, 'token':token}
        r = requests.get('%s/%s/' % (u, 'get_subjects'), data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_get_message(self):
        messageid = 1
        r = requests.get('%s/%s/%s' % (u, 'get_message', messageid))
        self.assertIsInstance(r.json(), list)

        messageid = 0
        r = requests.get('%s/%s/%s' % (u, 'get_message', messageid))
        self.assertEqual(r.json(), {'errormsg': u'资讯不存在'})

    def test_set_favorite(self):
        userid = 1
        token = '123456'
        data = {'userid': userid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_favorite'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, {u'errormsg': u'资讯不存在'})

        userid = 1
        messageid = 1
        token = '123456'
        data = {'userid': userid, 'messageid': messageid, 'token': token}
        r = requests.post('%s/%s' % (u, 'set_favorite'),
                          data=json.dumps(data)).json()
        self.assertEqual(r, True)

    def test_get_favorites(self):
        userid = 1
        token = '123456'
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s' % (u, 'get_favorites'),
                         data=json.dumps(data))

        self.assertIsInstance(r.json(), list)

    def test_get_competitions(self):
        userid = 1
        token = '123456'
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s' % (u, 'get_competitions'),
                         data=json.dumps(data))

        self.assertIsInstance(r.json(), list)

    def test_get_players(self):
        userid = 1
        token = '123456'
        competitionid = 1
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s/%s' % (u, 'get_players', competitionid),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_search_players(self):
        userid = 1
        token = '123456'
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s' % (u, 'search_players'),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

        userid = 1
        token = '123456'
        data = {'userid': userid, 'token': token, 'cname': u'刘佳'}
        r = requests.get('%s/%s' % (u, 'search_players'),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_vote(self):
        userid = 1
        token = '123456'
        playerid = 1
        data = {'userid': userid, 'token': token, 'playerid': playerid}
        r = requests.post('%s/%s' % (u, 'vote'),
                          data=json.dumps(data))
        self.assertEqual(r.json(), {'errormsg': u'已经投过票'})

    def test_get_user(self):
        userid = 1
        r = requests.get('%s/%s/%s' % (u, 'get_user', userid))
        self.assertIsInstance(r.json(), dict)

        userid = 0
        r = requests.get('%s/%s/%s' % (u, 'get_user', userid))
        self.assertEqual(r.json(), {'errormsg': u'用户不存在'})

    def test_register(self):
        cellphone = '13579246810'
        password = '1'
        data = {'cellphone': cellphone, 'password': password}
        r = requests.post('%s/%s' % (u, 'register'), data=data)
        self.assertEqual(r.json(), {"errormsg":
                                    "column username is not unique"})

        #cellphone = '13579246811'
        #password = '1'
        # data={'cellphone':cellphone,'password':password}
        #r = requests.post('%s/%s' % (u, 'register'),data=data)
        # self.assertEqual(r.json(),True)

    def test_if_cellphone_exist(self):
        userid = 1
        token = '123456'
        cellphone = '13579246810'
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s/%s' % (u, 'if_cellphone_exist', cellphone),
                         data=json.dumps(data))
        self.assertEqual(r.json(), True)

    # def test_login(self):
        #cellphone = '13579246810'
        #password = '1'
        # data={'cellphone':cellphone,'password':password}
        #r = requests.post('%s/%s' % (u, 'login'),data=data)
        # self.assertEqual(r.json(),{"errormsg":
                                   #"column username is not unique"})

    def test_modify_password(self):
        cellphone = '13579246810'
        oldpassword = '1'
        newpassword = '1'
        data = {'cellphone': cellphone, 'oldpassword': oldpassword,
                'newpassword': newpassword}
        r = requests.post('%s/%s' % (u, 'modify_password'), data=data)
        self.assertEqual(r.json(), True)

    def test_update_user_info(self):
        userid = '1'
        token = '123456'
        ename = 'home'
        data = {'userid': userid, 'token': token, 'ename': ename}
        r = requests.post('%s/%s' % (u, 'update_user_info'),
                          data=json.dumps(data))
        self.assertEqual(r.json(), True)

    def test_get_friends_list(self):
        userid = '1'
        token = '123456'
        data = {'userid': userid, 'token': token}
        r = requests.get('%s/%s' % (u, 'get_friends_list'),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_get_notifications(self):
        userid = '1'
        token = '123456'
        not_read = True
        data = {'userid': userid, 'token': token, 'not_read': not_read}
        r = requests.get('%s/%s' % (u, 'get_notifications'),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)

    def test_get_notification(self):
        userid = '1'
        token = '123456'
        notificationid = 1
        data = {'userid': userid, 'token': token,
                'notificationid': notificationid}
        r = requests.get('%s/%s' % (u, 'get_notification'),
                         data=json.dumps(data))
        self.assertIsInstance(r.json(), list)
        self.assertEqual(len(r.json()), 2)

    def test_invite(self):
        userid = 1
        token = '123456'
        target_cellphone = '13579246811'
        data = {'userid': userid, 'token': token,
                'target_cellphone': target_cellphone}
        r = requests.post('%s/%s' % (u, 'invite'),
                          data=json.dumps(data))
        self.assertEqual(r.json(), True)

    def test_pass_invite(self):
        userid = 2
        token = '123456'
        target_cellphone = '13579246810'
        data = {'userid': userid, 'token': token,
                'target_cellphone': target_cellphone}
        r = requests.post('%s/%s' % (u, 'pass_invite'),
                          data=json.dumps(data))
        self.assertEqual(r.json(), True)

    def test_deny_invite(self):
        userid = 2
        token = '123456'
        target_cellphone = '13579246810'
        data = {'userid': userid, 'token': token,
                'target_cellphone': target_cellphone}
        r = requests.post('%s/%s' % (u, 'deny_invite'),
                          data=json.dumps(data))
        self.assertEqual(r.json(), True)

    def test_get_user_by_uid_or_create(self):
        uid = '110120119'
        cellphone = '13579246812'
        data = {'cellphone': cellphone}
        r = requests.post(
            '%s/get_user_by_uid_or_create/%s' %
            (u, uid), data=json.dumps(data)).json()
        self.assertEqual(r['created'], False)

        uid = '110120120'
        cellphone = '13579246810'
        data = {'cellphone': cellphone}
        r = requests.post(
            '%s/get_user_by_uid_or_create/%s' %
            (u, uid), data=json.dumps(data)).json()
        self.assertEqual(r, {'errormsg': u'手机号码已存在'})


if __name__ == '__main__':
    unittest.main()
