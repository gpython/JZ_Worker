#encoding:utf-8
from django.db import models
from web import models as bbs_models
# Create your models here.

class CGroup(models.Model):
  name = models.CharField(max_length=64, verbose_name=u"群组名字")
  founder = models.ForeignKey(bbs_models.UserProfile, verbose_name=u"创始人")
  brief = models.TextField(max_length=1024, default="Nothing", verbose_name=u"简介")
  admin = models.ManyToManyField(bbs_models.UserProfile, related_name="group_admin", verbose_name=u"管理员")
  member = models.ManyToManyField(bbs_models.UserProfile, related_name="group_member", verbose_name=u"组员")
  member_limit = models.IntegerField(default=200l, verbose_name=u"人员限制")

  def __unicode__(self):
    return self.name

