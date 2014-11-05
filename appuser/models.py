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
        user.is_superuser=True
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
    ADMINS=(
        (1, u'网络编辑'),
        (2, u'内容审核'),
    )
    EDUCATION=(
        (0, u'无'),
        (1, u'小学'),
        (2, u'初中'),
        (3, u'高中'),
        (4, u'大学'),
    )
    DEGREE=(
        (0, u'无'),
        (1, u'学士'),
        (2, u'硕士'),
        (3, u'博士'),
    )
    RELIGION=(
        (0, u'无'),
        (1, u'佛教'),
        (2, u'伊斯兰教'),
        (3, u'基督教'),
        (4, u'道教'),
        (5, u'天主教'),
        (6, u'其他'),
    )
    STAR=(
        (0, u'白羊座'),
        (1, u'金牛座'),
        (2, u'双子座'),
        (3, u'巨蟹座'),
        (4, u'狮子座'),
        (5, u'处女座'),
        (6, u'天秤座'),
        (7, u'天蝎座'),
        (8, u'射手座'),
        (9, u'摩羯座'),
        (10, u'水瓶座'),
        (11, u'双鱼座'),
    )
    ZOD=(
        (0, u'鼠'),
        (1, u'牛'),
        (2, u'虎'),
        (3, u'兔'),
        (4, u'龙'),
        (5, u'蛇'),
        (6, u'马'),
        (7, u'羊'),
        (8, u'猴'),
        (9, u'鸡'),
        (10, u'狗'),
        (11, u'猪'),
    )
    BLOOD=(
        (0, u'A型'),
        (1, u'B型'),
        (2, u'AB型'),
        (3, u'O型'),
    )
    nick = models.CharField(max_length=60,verbose_name = '昵称', null=True, blank=True)
    cname = models.CharField(max_length=10,verbose_name = '真实名称', null=True, blank=True)
    gender = models.IntegerField(choices=GENDER,verbose_name = '性别', null=True, blank=True)
    email = models.EmailField(max_length=2048,verbose_name = '邮箱',unique=True, null=True, blank=True)
    cellphone = models.CharField(max_length=100, verbose_name = '注册号',unique=True)
    tel=models.IntegerField(verbose_name = '固定电话',blank=True,null=True)
    pic = models.ImageField(upload_to='myuser',verbose_name = '头像',blank=True,null=True)
    abroad = models.IntegerField(choices=CHOICES,verbose_name = '国内国外', default=0)
    country = models.CharField(max_length=256, verbose_name = '国家',null=True, blank=True)
    city = models.CharField(verbose_name = '城市',max_length=64, null=True, blank=True)
    zipcode= models.IntegerField(verbose_name = '邮政编码', null=True, blank=True)
    language = models.ForeignKey(Language,verbose_name = u'母语', null=True, blank=True)
    f_l = models.CharField(max_length=64,verbose_name = '外语', null=True, blank=True)
    education=models.IntegerField(choices=EDUCATION,verbose_name = '学历',blank=True,null=True)
    degree=models.IntegerField(choices=DEGREE,verbose_name = '学位',blank=True,null=True)
    birthday = models.DateField(verbose_name = '生日',blank=True,null=True)
    born_place = models.CharField(max_length=64,verbose_name = '籍贯', null=True, blank=True)    
    university = models.CharField(max_length=256, verbose_name = '大学',null=True, blank=True)
    career = models.CharField(max_length=100,verbose_name = '职业', null=True, blank=True)
    religion=models.IntegerField(choices=RELIGION,verbose_name = '宗教',blank=True,null=True)
    blood=models.IntegerField(choices=BLOOD,verbose_name = '血型',blank=True,null=True)
    star=models.IntegerField(choices=STAR,verbose_name = '星座',blank=True,null=True)
    zod=models.IntegerField(choices=ZOD,verbose_name = '属相',blank=True,null=True)
    inte = models.CharField(max_length=100,verbose_name = '兴趣', null=True, blank=True)
    desc = models.CharField(max_length=200,verbose_name = '介绍', null=True, blank=True)
    point= models.IntegerField(verbose_name = '积分',default=0)
    hanbi=models.IntegerField(verbose_name = '汉币',default=0)
    level= models.IntegerField(verbose_name = '级别',default=1)
    installdate = models.DateTimeField(verbose_name = '安装时间',null=True, blank=True)
    pubdate = models.DateTimeField(auto_now_add=True,verbose_name = '注册时间',)
    favorites = models.ManyToManyField(Message,verbose_name = u'收藏资讯', null=True, blank=True)
    is_active = models.BooleanField(default=True,verbose_name = u'是否活跃用户')
    is_admin = models.BooleanField(default=False,verbose_name = u'管理员(网络编辑或内容审核)')
    admin_type=models.IntegerField(choices=ADMINS,verbose_name = u'管理员类型',null=True,blank=True)
    is_superuser = models.BooleanField(default=False,verbose_name = u'超级管理员(全部权限)')

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
        if self.is_superuser and self.is_active:
            return True
        elif self.is_admin and self.is_active and self.admin_type==1:
            if perm[:7]=='message' or perm[:11]=='competition':
                return True
            else:
                return False
        elif self.is_admin and self.is_active and self.admin_type==2:
            if  perm=='competition.change_player' or perm=='competition.change_competition' or perm=='competition.change_competitionsubject' or perm=='message.change_language'\
            or perm=='message.change_message' or perm=='message.change_messagecontent' or perm=='message.change_messagesubject' or perm=='message.change_localmedia':
                return True
            else:
                return False
        else:
            return False

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


