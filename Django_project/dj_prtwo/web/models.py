#encoding:utf-8
from django.db import models

#ForeignKey 查询
# Create your models here.
class UserType(models.Model):
  name = models.CharField(max_length = 50)

class UserInfo(models.Model):
  username = models.CharField(max_length = 50)
  password = models.CharField(max_length = 50)
  email = models.EmailField()
  user_type = models.ForeignKey('UserType')

class UserGroup(models.Model):
  GroupName = models.CharField(max_length = 50)
  user = models.ManyToManyField('UserInfo')

#UserType id大于5的所有用户信息
#UserInfo.objects.filter(user_type__id__gt = 5)
#查询UserType name中包含A的用户信息
#UserInfo.objects.filter(user_type__name__contains = 'A')
#UserInfo.objects.filter(user_type__name = 'sb')
#UserInfo.objects.filter(user_type__name = 'sb').values('username', 'email')

#ManyToManyField
