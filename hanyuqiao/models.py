# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.TextField(max_length=64)
    index = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'语言'


class MessageSubject(models.Model):
    title = models.CharField(max_length=512)
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'资讯主题'


class Message(models.Model):
    messagesubject = models.ForeignKey(MessageSubject)
    def __unicode__(self):
        if self.messagecontent_set.exists():
            return self.messagecontent_set.all()[0].title
        return u'空白'

    class Meta:
        verbose_name = u'资讯'


class MessageContent(models.Model):
    message = models.ForeignKey(Message)
    language = models.ForeignKey(Language)
    title = models.CharField(max_length=512)
    author = models.CharField(max_length=512)
    source = models.CharField(max_length=512)
    admin = models.CharField(max_length=512)
    passed = models.BooleanField(default=False)
    text = models.TextField()
    postdate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @property
    def medias(self):
        print self.media_set.all().values()
        return list(self.media_set.all().values())

    class Meta:
        verbose_name = u'资讯内容(特定语言)'


class Media(models.Model):
    MEDIATYPE=(
        (1,'图片'),
        (2,'语音'),
        (3,'视频'),
    )
    mediatype = models.IntegerField(choices=MEDIATYPE)
    mediafile = models.FileField(upload_to='.')
    message = models.ForeignKey(MessageContent)

    def __unicode__(self):
        return u'%s' % self.mediafile


class MyUser(models.Model):
    GENDER = (
        (0, u'男'),
        (1, u'女'),
    )
    user = models.OneToOneField(User)
    friends = models.ManyToManyField("self", null=True, blank=True)
    pic = models.ImageField(upload_to='.')
    language = models.ForeignKey(Language, null=True, blank=True)
    favorites = models.ManyToManyField(Message, null=True, blank=True)
    cname = models.CharField(max_length=32, null=True, blank=True)
    ename = models.CharField(max_length=256, null=True, blank=True)
    nick = models.CharField(max_length=32, null=True, blank=True)
    uid = models.CharField(max_length=128, unique=True)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    desc = models.CharField(max_length=2048, null=True, blank=True)
    email = models.EmailField(max_length=2048, null=True, blank=True)
    cellphone = models.CharField(max_length=18,unique=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    university = models.CharField(max_length=256, null=True, blank=True)
    career = models.CharField(max_length=256, null=True, blank=True)
    installdate = models.DateTimeField(null=True, blank=True)
    registerdate = models.DateTimeField(auto_now_add = True,null=True, blank=True)
    token = models.CharField(max_length=512, null=True, blank=True)

    def __unicode__(self):
        return self.cellphone

    class Meta:
        verbose_name = u'用户'


class Notification(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField()
    postdate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'通知'


class ExtraNotification(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    notification = models.ForeignKey(Notification)
    hasread = models.BooleanField(default=False)

    def __unicode__(self):
        return self.notification.title

    class Meta:
        verbose_name = u'个人通知'


class Version(models.Model):
    version = models.CharField(max_length=16)

    def __unicode__(self):
        return self.version

    def __cmp__(self, other):
        if self.version.split('.') == other.version.split('.'):
            return 0
        if self.version.split('.') > other.version.split('.'):
            return 1
        return -1

    class Meta:
        verbose_name = u'版本'


class IntroductionImage(models.Model):
    introduction = models.ForeignKey(Version)
    pic = models.ImageField(upload_to='.')

    def __unicode__(self):
        return '%s[%s]'%(self.introduction.version,self.pic.url)

    class Meta:
        verbose_name = u'引导页图片'


class Competition(models.Model):
    subject = models.CharField(max_length=512)
    category = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    startdate = models.DateField()
    enddate = models.DateField()

    def __unicode__(self):
        return u'[%s]%s' % (self.subject, self.title)

    class Meta:
        verbose_name = u'比赛'


class Player(models.Model):
    GENDER = (
        (0, u'男'),
        (1, u'女'),
    )
    competition = models.ForeignKey(Competition)
    votes = models.IntegerField(default=0)
    whovotes = models.ManyToManyField(MyUser, null=True, blank=True)
    sn = models.AutoField(unique=True, primary_key=True)
    cname = models.CharField(max_length=32, null=True, blank=True)
    ename = models.CharField(max_length=256, null=True, blank=True)
    weibo = models.CharField(max_length=128, null=True, blank=True)
    qq = models.CharField(max_length=16, null=True, blank=True)
    pic = models.ImageField(upload_to='.', null=True, blank=True)
    birthyear = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    university = models.CharField(max_length=256, null=True, blank=True)
    competition_area = models.CharField(max_length=256, null=True, blank=True)
    ci = models.CharField(max_length=256, null=True, blank=True)
    tutor = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.cname

    class Meta:
        verbose_name = u'选手'


class PlayerInfo(models.Model):
    player = models.ForeignKey(Player)
    language = models.ForeignKey(Language)
    interist = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = u'选手信息(特定语言)'

