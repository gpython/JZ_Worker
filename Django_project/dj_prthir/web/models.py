#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
  """帖子板块"""
  name = models.CharField(max_length=64, unique=True)
  admin = models.ManyToManyField('UserProfile')
  def __unicode__(self):
    return self.name


class UserGroup(models.Model):
  """用户组"""
  name = models.CharField(max_length=64, unique=True)
  def __unicode__(self):
    return self.name


class UserProfile(models.Model):
  """账户信息"""
  user = models.OneToOneField(User)
  name = models.CharField(max_length=32)
  groups = models.ManyToManyField('UserGroup')
  def __unicode__(self):
    return self.name


class Article(models.Model):
  """
  帖子
  """
  title = models.CharField(max_length=255, unique=True, verbose_name=u'文章标题')
  category = models.ForeignKey('Category', verbose_name=u'板块')
  head_img = models.CharField(max_length=255)
  summary = models.CharField(max_length=255)
  content = models.TextField(verbose_name=u'内容')
  author = models.ForeignKey('UserProfile')
  publish_date = models.DateTimeField(auto_now=True)
  hidden = models.BooleanField(default=True)
  priority = models.IntegerField(default=1000, verbose_name=u'优先级')

  def __unicode__(self):
    return "<title: %s, author: %s>" %(self.title, self.author)

class Comment(models.Model):
  """
  评论
  多个评论对应一个文章 多对一单向外键关联
  多个评论作者对应一个文章 多对一单向外键关联
  模板中文章的评论数 某篇文章评论集合 comment_set
  article.comment_set.select_related.count
  """
  article = models.ForeignKey('Article')
  user = models.ForeignKey('UserProfile')
  parent_comment = models.ForeignKey('self', related_name='p_comment', blank=True, null=True)
  comment = models.TextField(max_length=1000)
  date = models.DateTimeField(auto_now=True)
  def __unicode__(self):
    return "<%s, User:%s>" %(self.comment, self.user)

class ThumbUp(models.Model):
  """
  攒
  多个点赞对应一篇文章 多对一单向外键关联
  多个点赞用户对应一篇文章 多对一单向外键关联
  模板中获取点赞数量  thumbup_set集合
  article.thumbup_set.select_related.count
  """
  article = models.ForeignKey('Article')
  user = models.ForeignKey('UserProfile')
  date = models.DateTimeField(auto_now=True)
  def __unicode__(self):
    return "<User: %s>" %(self.user)





