# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=512,verbose_name = u'语言')
    index = models.IntegerField(verbose_name = u'数字索引')
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'语言'
        verbose_name_plural = "语言"


class MessageSubject(models.Model):
    title = models.CharField(max_length=512,verbose_name = u'名称')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'资讯主题'
        verbose_name_plural = "资讯主题"


class Message(models.Model):
    messagesubject = models.ForeignKey(MessageSubject,verbose_name = u'资讯主题')
    title = models.CharField(max_length=512,verbose_name = u'标题')
    pubDate = models.DateTimeField(auto_now_add=True)
    postdate = models.DateTimeField(auto_now=True,verbose_name = u'修改日期')    
    def __unicode__(self):
        return self.title
        

    class Meta:
        verbose_name = u'资讯'
        verbose_name_plural = "资讯"


class MessageContent(models.Model):
    CHOICES = (
        (True, '通过审核'),
        (False, '等待审核'),
        
    )
    message = models.ForeignKey(Message,verbose_name = u'源资讯')
    language = models.ForeignKey(Language,verbose_name = u'语言分类')
    title = models.CharField(max_length=512,verbose_name = u'标题')
    author = models.CharField(max_length=512,verbose_name = u'作者')
    source = models.CharField(max_length=512, null=True, blank=True,verbose_name = u'来源')
    admin = models.CharField(max_length=512,verbose_name = u'管理')
    passed = models.BooleanField(choices=CHOICES,default=False,verbose_name = u'审核')
    text = models.TextField(verbose_name = u'内容')
    pubDate = models.DateTimeField(auto_now_add=True)
    postdate = models.DateTimeField(auto_now=True,verbose_name = u'修改日期')

    def __unicode__(self):
        return self.title

    @property
    def messageid(self):
        return self.message.id

    @property
    def medias(self):
        return list(self.localmedia_set.all().values()) + \
            list(self.remotemedia_set.all().values())

    class Meta:
        verbose_name = u'资讯内容(特定语言)'
        verbose_name_plural = "资讯内容(特定语言)"


class LocalMedia(models.Model):
    MEDIATYPE = (
        (1, '图片'),
    )
    mediatype = models.IntegerField(choices=MEDIATYPE,verbose_name = u'类型')
    mediafile = models.FileField(upload_to='.', null=True, blank=True,verbose_name = u'文件上传')
    message = models.ForeignKey(MessageContent,verbose_name = u'资讯')

    def __unicode__(self):
        return u'%s' % self.mediafile
    class Meta:
        verbose_name = u'资讯图片'
        verbose_name_plural = "资讯图片"
class RemoteMedia(models.Model):
    MEDIATYPE = (
        (2, '语音'),
        (3, '视频'),
    )
    mediatype = models.IntegerField(choices=MEDIATYPE,verbose_name = u'类型')
    remotefile = models.CharField(max_length=1024,verbose_name = u'文件', null=True, blank=True)
    message = models.ForeignKey(MessageContent,verbose_name = u'资讯')

    def __unicode__(self):
        return u'%s' % self.remotefile
    class Meta:
        verbose_name = u'资讯视频'
        verbose_name_plural = "资讯视频"
