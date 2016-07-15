#encoding:utf-8

from django.db import models

class UserType(models.Model):
  name = models.CharField(max_length=50)

class Group(models.Model):
  name = models.CharField(max_length=50)

class UserInfo(models.Model):
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  gender = models.BooleanField(default=False)
  age = models.IntegerField(default=19)
  memo = models.TextField(default='xxxx')
  createtime = models.DateTimeField(default='2016-06-06 06:06:06')
  typeId = models.ForeignKey(UserType)
  group_relation = models.ManyToManyField(Group)

class Asset(models.Model):
  hostname = models.CharField(max_length=256)
  create_time = models.DateField(auto_now_add=True)
  update_time = models.DateField(auto_now=True)

class UserInfo_Temp(models.Model):
  GENDER_CHOICE = (
    (u'M', u'Male'),
    (u'F', u'Female'),
  )
  gender = models.CharField(max_length=2, choices=GENDER_CHOICE)



"""
class User(models.Model):
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  group_relation = models.ManyToManyField(Group)
"""
"""
class UserType(models.Model):
  name = models.CharField(max_length = 50)

class UserInfo(models.Model):
  username = models.CharField(max_length = 50)
  password = models.CharField(max_length = 50)
  email = models.EmailField()
  user_type = models.ForeignKey(UserType)

class UserGroup(models.Model):
  GroupName = models.CharField(max_length = 50)
  user = models.ManyToManyField(UserInfo)

class Asset(models.Model):
  hostname = models.CharField(max_length = 256)
  ip = models.IPAddressField()
  user_group = models.ForeignKey(UserGroup)
"""

