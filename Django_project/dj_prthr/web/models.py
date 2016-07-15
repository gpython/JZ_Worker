#encoding:utf-8
from django.db import models

# Create your models here.

class UserType(models.Model):
  name = models.CharField(max_length = 50)

class UserInfo(models.Model):
  username = models.CharField(max_length = 50)
  password = models.CharField(max_length = 50)
  email = models.EmailField()
  user_type = models.ForeignKey('UserType')

class UserGroup(models.Model):
  groupname = models.CharField(max_length = 50)
  user = models.ManyToManyField('UserInfo')

class Host(models.Model):
  hostname = models.CharField(max_length = 256)
  ip = models.GenericIPAddressField ()


####################################
class Article(models.Model):
  """
  文章
  """
  title = models.CharField(max_length=255, unique = True, verbose_name=u"文章标题")
  category = models.ForeignKey('Category', verbose_name=u" ForeignKey category")
  head_img = models.ImageField(upload_to = "uploads")
  content = models.TextField(verbose_name=u"content")
  author = models.ForeignKey("UserProfile", verbose_name=u" ForeignKey author")
  publish_date = models.DateField(auto_now = True)
  hidden  = models.BooleanField(default=True)
  priority = models.IntegerField(default=1000, verbose_name=u"priority")

  def __unicode__(self):
    return "<%s, author: %s>" %(self.title, self.author)


class UserProfile(models.Model):
  pass

class Comment(models.Model):
  pass

class Category(models.Model):
  """
  板块名字
  """
  name = models.CharField(max_length = 64, unique = True)
  admin = models.ForeignKey('UserProfile')
  def __unicode__(self):
    return self.name

  pass

class UserGroup(models.Model):
  pass

class
