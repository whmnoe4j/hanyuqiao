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
        (2, '申请审核'),
        (3, '通过'),
        (1, '拒绝'),
        
    )
    message = models.ForeignKey(Message,verbose_name = u'源资讯')
    language = models.ForeignKey(Language,verbose_name = u'语言分类')
    title = models.CharField(max_length=512,verbose_name = u'标题')
    author = models.CharField(max_length=512,verbose_name = u'作者')
    source = models.CharField(max_length=512, null=True, blank=True,verbose_name = u'来源')
    passed = models.IntegerField(choices=CHOICES,default=2,verbose_name = u'审核状态')
    pubDate = models.DateTimeField(auto_now_add=True)
    postdate = models.DateTimeField(auto_now=True,verbose_name = u'修改日期')
    def __unicode__(self):
        return self.title

    @property
    def messageid(self):
        return self.message.id

    @property
    def medias(self):
        return list(self.localmedia_set.all().values())

    class Meta:
        verbose_name = u'资讯内容(特定语言)'
        verbose_name_plural = "资讯内容(特定语言)"


class LocalMedia(models.Model):
    MEDIATYPE = (
        (1, '图片+文字'),
        (2, '语音+文字'),
        (3, '视频+文字'),
        (4, '文字'),
    )
    message = models.ForeignKey(MessageContent,verbose_name = u'资讯')
    mediatype = models.IntegerField(choices=MEDIATYPE,verbose_name = u'类型')
    text = models.TextField(verbose_name = u'文本')
    pictitle= models.CharField(max_length=100,verbose_name = u'图片标题', null=True, blank=True)
    mediafile = models.ImageField(upload_to='Image', null=True, blank=True,verbose_name = u'图片上传')
    remotefile = models.CharField(max_length=1024,verbose_name = u'语音视频文件地址', null=True, blank=True)
    def __unicode__(self):
        return u'%s的片段' % self.message.title
    class Meta:
        verbose_name = u'图文片段'
        verbose_name_plural = "图片片段"

