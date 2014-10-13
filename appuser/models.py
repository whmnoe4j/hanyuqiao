# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from message.models import Language,Message
from hanyuqiao import settings
class MyUserManager(BaseUserManager):
    def create_user(self, cellphone, password):
        if not cellphone:
            raise ValueError('Users must have an phoneNumber')
        user = self.model(cellphone=cellphone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, cellphone, password):
        user = self.create_user(cellphone, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    GENDER = (
        (0, u'男'),
        (1, u'女'),
    )
    CHOICES = (
        (0, u'国内'),
        (1, u'国外'),
    )
    cname = models.CharField(max_length=32,verbose_name = '名称', null=True, blank=True)
    ename = models.CharField(max_length=256,verbose_name = '英文名', null=True, blank=True)
    nick = models.CharField(max_length=32,verbose_name = '昵称', null=True, blank=True)
    email = models.EmailField(max_length=2048,verbose_name = '邮箱',unique=True, null=True, blank=True)
    cellphone = models.CharField(max_length=100, verbose_name = '手机号',unique=True)
    pic = models.ImageField(upload_to='.',verbose_name = '头像')
    language = models.ForeignKey(Language,verbose_name = u'母语', null=True, blank=True)
    f_l = models.CharField(max_length=64,verbose_name = '外语', null=True, blank=True)
    gender = models.IntegerField(choices=GENDER,verbose_name = '性别', null=True, blank=True)
    abroad = models.IntegerField(choices=CHOICES,verbose_name = '国内国外', default=0)
    birthday = models.DateField(verbose_name = '生日',blank=True,null=True)
    born_place = models.CharField(max_length=64,verbose_name = '籍贯', null=True, blank=True)    
    city = models.CharField(verbose_name = '城市',max_length=64, null=True, blank=True)
    zipcode= models.IntegerField(verbose_name = '邮政编码', null=True, blank=True)
    country = models.CharField(max_length=256, verbose_name = '国家',null=True, blank=True)
    university = models.CharField(max_length=256, verbose_name = '大学',null=True, blank=True)
    career = models.CharField(max_length=100,verbose_name = '爱好', null=True, blank=True)
    point= models.IntegerField(verbose_name = '积分',default=0)
    desc = models.CharField(max_length=200,verbose_name = '介绍', null=True, blank=True)
    installdate = models.DateTimeField(verbose_name = '安装时间',null=True, blank=True)
    pubdate = models.DateTimeField(auto_now_add=True,verbose_name = '注册时间',)
    favorites = models.ManyToManyField(Message,verbose_name = u'收藏资讯', null=True, blank=True)
    friends = models.ManyToManyField("self",verbose_name = u'好友', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'cellphone'

    objects = MyUserManager()
    def __unicode__(self):
        if self.cname:
            return self.cname
        else:
            return self.cellphone
    def get_full_name(self):
        return self.cname

    def get_short_name(self):
        return self.cname



    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"  # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
            "Does the user have permissions to view the app ‘app_label‘?"  # Simplest possible answer: Yes, always
            return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = "用户"
class MyUserToken(models.Model):
    phone=models.CharField(max_length=20,unique=True)
    token=models.CharField(max_length=20)
    pub_date=models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.phone
    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = "验证码"

class Notification(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField()
    postdate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = "通知"

class ExtraNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    notification = models.ForeignKey(Notification)
    hasread = models.BooleanField(default=False)

    def __unicode__(self):
        return self.notification.title

    class Meta:
        verbose_name = u'个人通知'
        verbose_name_plural = "个人通知"
