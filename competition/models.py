# -*- coding: utf-8 -*-
from django.db import models
from hanyuqiao import settings
from message.models import Language
class Competition(models.Model):
    subject = models.CharField(max_length=512,verbose_name = u'主题')
    category = models.CharField(max_length=512,verbose_name = u'类型')
    title = models.CharField(max_length=512,verbose_name = u'标题')
    startdate = models.DateField(verbose_name = u'开始日期')
    enddate = models.DateField(verbose_name = u'截止日期')

    def __unicode__(self):
        return u'[%s]%s' % (self.subject, self.title)

    class Meta:
        verbose_name = u'比赛'
        verbose_name_plural = "比赛"

class Player(models.Model):
    GENDER = (
        (0, u'男'),
        (1, u'女'),
    )
    CHOICES = (
        (True, u'已淘汰'),
        (False, u'未淘汰'),
    )
    AREAS = (
        (1, u'亚洲'),
        (2, u'欧洲'),
        (3, u'美洲'),
        (4, u'非洲'),
        (5, u'大洋洲'),
    )
    sn = models.IntegerField(unique=True,verbose_name = u'选手编号')
    competition = models.ForeignKey(Competition,verbose_name = u'比赛')
    cname = models.CharField(max_length=32,verbose_name = u'名称')
    ename = models.CharField(max_length=256, verbose_name = u'英文名称',null=True, blank=True)
    votenum = models.IntegerField(verbose_name = u'获得票数',default=0)
    isout = models.BooleanField(choices=CHOICES,default=False,verbose_name = u'是否被淘汰')
    whovotes = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name = u'投票人', null=True, blank=True)
    weibo = models.CharField(max_length=128, verbose_name = u'微博',null=True, blank=True)
    qq = models.CharField(max_length=16,verbose_name = u'qq', null=True, blank=True)
    pic = models.ImageField(upload_to='.', verbose_name = u'头像',null=True, blank=True)
    birthyear = models.IntegerField(verbose_name = u'出生年',null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, verbose_name = u'性别',null=True, blank=True)
    country = models.CharField(max_length=256,verbose_name = u'国家', null=True, blank=True)
    university = models.CharField(max_length=256, verbose_name = u'大学',null=True, blank=True)
    ci = models.CharField(max_length=256,verbose_name = u'推荐孔院', null=True, blank=True)
    tutor = models.CharField(max_length=256, verbose_name = u'指导教师',null=True, blank=True)
    area = models.IntegerField(choices=AREAS,verbose_name = u'赛区', null=True, blank=True)


    def __unicode__(self):
        return self.cname

    class Meta:
        verbose_name = u'比赛选手'
        verbose_name_plural = "比赛选手"


class PlayerInfo(models.Model):
    player = models.ForeignKey(Player,verbose_name = u'选手')
    language = models.ForeignKey(Language,verbose_name = u'语言')
    interist = models.TextField(verbose_name = u'兴趣',null=True, blank=True)
    desc = models.TextField(verbose_name = u'介绍',null=True, blank=True)

    class Meta:
        verbose_name = u'选手信息(特定语言)'
        verbose_name_plural = "选手信息(特定语言)"
