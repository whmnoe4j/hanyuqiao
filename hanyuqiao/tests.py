# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from hanyuqiao.models import Version, Notification, ExtraNotification,\
    Message, MessageContent, Competition, Player, MyUser, Language, MessageSubject, PlayerInfo
import json
from django.contrib.auth.models import User
import datetime


class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.language = Language.objects.create(name='english', index=1)

        self.version = Version.objects.create(version='3.1.2')

        self.messagesubject = MessageSubject.objects.create(title='football')
        self.message = Message.objects.create(
            messagesubject=self.messagesubject)
        self.content = MessageContent.objects.create(
            message=self.message,
            language=self.language,
            title='title',
            text='text')

        user = User.objects.create_user(
            username='13888888888',
            password='111111')
        user.save()
        myuser = MyUser(user=user, cellphone='13888888888')
        myuser.token = '123456'
        myuser.uid = '111111'
        myuser.save()
        self.myuser = myuser

        competition = Competition.objects.create(
            subject='football', title='title', startdate=datetime.date(
                2014, 8, 8), enddate=datetime.date(
                2014, 12, 12))
        competition.save()
        self.competition = competition
        self.player = Player.objects.create(competition=self.competition, sn=1)
        PlayerInfo.objects.create(
            player=self.player,
            language=self.language,
            desc='足球')

        self.notification = Notification.objects.create(
            title='title',
            text='text')
        self.extra_no = ExtraNotification.objects.create(
            user=self.myuser,
            notification=self.notification)

    def test_if_introduction_exist(self):
        response = self.client.get('/if_introduction_exist/3.1.2')
        self.assertEqual(json.loads(response.content), True)
        response = self.client.get('/if_introduction_exist/3.1.3')
        self.assertEqual(json.loads(response.content), False)

    def test_get_language_list(self):
        response = self.client.get('/get_language_list')
        self.assertEqual(
            json.loads(response.content), [{'id': 1, 'name': 'english'}])

    def test_newest_version(self):
        r = self.client.get('/newest_version')
        self.assertEqual(r.content, '3.1.2')

    def test_get_user_by_uid_or_create(self):
        data = json.dumps(
            {'cellphone': '13888888888', 'userid': 1, 'token': '123456'})
        r = self.client.options('/get_user_by_uid_or_create/111111', data=data)
        self.assertEqual(
            json.loads(
                r.content), {
                u'token': u'123456', u'userid': 1, u'created': False})

    def test_set_language(self):
        data = json.dumps(
            {'cellphone': '13888888888', 'userid': 1, 'token': '123456',
             'languageid': 1})
        r = self.client.options('/set_language', data=data)
        self.assertEqual(json.loads(r.content), True)
        user = MyUser.objects.get(cellphone='13888888888')
        self.assertEqual(user.language.id, 1)

    def test_translate(self):
        r = self.client.get('/translate/1/1')
        self.assertEqual(json.loads(r.content), {'title': self.content.title,
                                                 'text': self.content.text})

    def test_getmessages(self):
        data = json.dumps(
            {'cellphone': '13888888888', 'userid': 1, 'token': '123456',
             'subject': 'football'})
        r = self.client.options('/get_messages', data=data)
        self.assertEqual(r.content,
                         json.dumps([{u'postdate': self.content.postdate.isoformat(),
                                      u'title': self.content.title,
                                      u'text': self.content.text,
                                      u'min_index': 1,
                                      u'language_id': 1,
                                      u'id': 1,
                                      u'message_id': 1}]))

    def test_get_message(self):
        r = self.client.get('/get_message/1')
        self.assertEqual(r.content,
                         json.dumps([{u'postdate': self.content.postdate.isoformat(),
                                      u'title': self.content.title,
                                      u'text': self.content.text,
                                      u'language_id': 1,
                                      u'id': 1,
                                      u'message_id': 1}]))

    def test_set_favorite_and_get_favorites(self):
        data = json.dumps(
            {'cellphone': '13888888888', 'userid': 1, 'token': '123456',
             'messageid': 1, 'languageid': 1})
        self.client.options('/set_language', data=data)
        r = self.client.options('/set_favorite', data=data)
        self.assertEqual(r.content, json.dumps(True))
        self.assertEqual(self.myuser.favorites.all()[0].id, 1)
        r = self.client.options('/get_favorites', data=data)
        self.assertEqual(r.content, json.dumps([{'id': 1, 'title': 'title'}]))

    def test_get_competitions(self):
        data = json.dumps({'userid': 1, 'token': '123456', })
        r = self.client.options('/get_competitions',data)
        self.assertEqual(r.content,
                         json.dumps([{'id': 1,
                                      'subject': self.competition.subject,
                                      'title': self.competition.title,
                                      'category':'',
                                      'startdate': self.competition.startdate.isoformat(),
                                      'enddate': self.competition.enddate.isoformat()}]))

    def test_get_players_and_search_players(self):
        r = self.client.get('/get_players/1')
        self.assertEqual(json.loads(r.content)[0]['competition_id'], 1)
        data = json.dumps({'userid': 1, 'token': '123456', 'desc': u'足球'})
        r = self.client.options('/search_players', data=data)
        self.assertEqual(json.loads(r.content)[0]['id'], 1)

    def test_vote(self):
        data = json.dumps({'userid': 1, 'token': '123456', 'playerid': 1})
        r = self.client.options('/vote', data=data)
        self.assertEqual(r.content, json.dumps(True))
        player = Player.objects.get(id=1)
        self.assertEqual(player.votes, 1)

    def test_get_user(self):
        r = self.client.get('/get_user/1')
        self.assertEqual(json.loads(r.content)['id'], 1)

    def test_register(self):
        r = self.client.post(
            '/register',
            data={
                'cellphone': '13666666666',
                'password': '111111'})
        user = MyUser.objects.get(id=2)
        self.assertEqual(user.cellphone, '13666666666')
        self.assertEqual(
            self.client.login(
                username='13666666666',
                password='111111'),
            True)

    def test_if_cellphone_exist(self):
        r = self.client.get('/if_cellphone_exist/13888888888')
        self.assertEqual(r.content, json.dumps(True))

    def test_login(self):
        r = self.client.post(
            '/login',
            data={
                'cellphone': '13888888888',
                'password': '111111'})
        user = MyUser.objects.get(cellphone='13888888888')
        r = json.loads(r.content)
        self.assertEqual(r, {'token':user.token,'userid':user.id})

    def test_modify_password(self):
        r = self.client.post(
            '/modify_password',
            data={
                'cellphone': '13888888888',
                'oldpassword': '111111',
                'newpassword': '222222'})
        self.assertEqual(r.content, json.dumps(True))

    def test_update_user_info(self):
        r = self.client.post(
            '/login',
            data={
                'cellphone': '13888888888',
                'password': '111111'}).content
        token = json.loads(r)['token']
        data = json.dumps({'userid': 1, 'token': token, 'cname': 'li'})
        r = self.client.options('/update_user_info', data=data)
        self.assertEqual(r.content, json.dumps(True))

    def test_get_notifications(self):
        r = self.client.post(
            '/login',
            data={
                'cellphone': '13888888888',
                'password': '111111'}).content
        token = json.loads(r)['token']
        data = json.dumps({'userid': 1, 'token': token})
        r = self.client.options('/get_notifications', data=data)
        self.assertEqual(json.loads(r.content)[0][0], 1)

    def test_invite_and_pass_and_deny(self):
        self.client.post(
            '/register',
            data={
                'cellphone': '13666666666',
                'password': '111111'})
        r = self.client.post(
            '/login',
            data={
                'cellphone': '13888888888',
                'password': '111111'}).content
        token = json.loads(r)['token']
        data = json.dumps(
            {'userid': 1, 'token': token, 'target_cellphone': '13666666666'})
        r = self.client.options('/invite', data=data)
        self.assertEqual(r.content, json.dumps(True))
        r = self.client.options('/pass_invite', data=data)
        self.assertEqual(r.content, json.dumps(True))
