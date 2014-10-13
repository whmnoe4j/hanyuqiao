# -*- coding: utf-8 -*-

from django.db import models
from message.models import Message
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
        verbose_name_plural = "版本"

class IntroductionImage(models.Model):
    introduction = models.ForeignKey(Version)
    pic = models.ImageField(upload_to='InfoImg')
    message=models.ForeignKey(Message,verbose_name = u'资讯')

    def __unicode__(self):
        return '%s[%s]' % (self.introduction.version, self.pic.url)

    class Meta:
        verbose_name = u'引导页图片'
        verbose_name_plural = "引导页"

