#
Django
##############################################################
pip install -i http://pypi.douban.com/simple/ django==1.8



django-admin startproject sitename

python manager.py runserver 0.0.0.0:80
python manager.py startapp appname

TIME_ZONE = 'Asia/Shanghai'


工程下urls 路由分发到对应app下
from dj_project import views
import web
import ad

urlpatterns = [
  url(r'^web/', include('web.urls')),
  url(r'^ad/', include('ad.urls')),
]

APP 下路由规则
from django.conf.urls import patterns, include, url
from web import views

urlpatterns = patterns('',
  url(r'^index/', views.index),
  url(r'^login/', views.login),
  url(r'list/(\d*)/', views.list),
)

def list(request, page):
  page = int(page)

创建数据库
配置文件settings里连接数据库

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj',
        'USER': 'root',
        'PASSWORD': 'google',
        'HOST': '192.168.47.9',
        'PORT': 3306,
    }
}

setting INSTALLED_APPS 里添加指定model的app
INSTALLED_APPS = (
  ....
  'web',
)

创建model
from django.db import models

class UserInfo(models.Model):
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)

执行命令
#python manage.py syncdb
python manage.py makemigrations
python manage.py migrate

先添加字段执行migrate 时 需要添加默认值

#################################################################
外键关联 一对多 ForeignKey
  (用户 与 用户类型) 一个用户属于一种用户类型

class UserType(models.Model):
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

  ForeignKey 外键
  UserType中的一条记录 可以对应UserInfo中的多条记录

用户类型一对多用户
用户表 类型 typeId 外键关联到用户类型表 Foreignkey

多对多
  (用户 与 用户组) 一个用户可以属于多个用户组 ManyToManyField
  借助另外一张表  Django 会自动创建第三张表
  Group User ==> Group_User
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

Model_table.objects.create(hostname = name)
Model_table.objects.get(id = id).delete()
Model_table.objects.filter(id__gt = id).update(hostname = name)
Model_table.objects.filter(hostname__contains = hostname)
Model_table.object.all()[0:4]

get(条件)
获取单条数据 一个对象

filter(条件)
多条数据




Django1.8 模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

{% for item in data %}
  {{ item.id }}
  {{ item.name }}
{% endfor %}

{% if orderinfo %}
{% else %}
{% endif %}

########################
request.method == 'POST'
request.method == 'GET'
user = request.POST.get('username', None)
passwd = request.POST.get('password', None)

######################
from django import forms

class RegisterForm(forms.Form):
  username = forms.CharField()
  email = forms.EmailField(required = True)

#
#all(['google', '', 'yahoo', 'python'])


cnt = filter(username=name).count()
########################
获取group组对象 然后在赋值
groupObj = models.UserGroup.objects.get(id = groupId)
models.Asset.objects.create(hostname=hostname,
  ip = ip,
  user_group = groupObj
)

跨表查询 filter 用 双下划线 __
#  获取所有Admin用户组的所有用户信息
#  obj = models.Asset.objects.filter(user_group__GroupName = 'Admin')

跨表取值(filter 得到的对象 里取值) 点 .
  obj.user_group.id
  obj.user_group.GroupName


保存会话
request.session['key'] = value
request.session['key'] = {'key':'value'}
获取会话key
get_sess = request.session.get('key', None)
删除session
del request.session['key']

表单提交csrf
{% csrf_token %}

settings.py
#设置session过期时间 秒
SESSION_COOKIE_AGE = 3600

模板当前url
{{ request.path }}

url中指定name = value 在模板中可使用
href="{% url 'value' parament %}"

外键 多对一单向外键关联

######################################CSS#################################
padding 内边距 上 右 下 左
margin  外边距 上 右 下 左

隐藏元素 - display:none或visibility:hidden
display:none  不显示 不占用空间
visibility: hidden 隐藏某个元素 仍占用空间

块 和 内联 元素
块(block)元素是一个元素 占用全部宽度 在前后都是换行符
块元素例子
<h>
<p>
<li>
<div>

内联(inline)元素只需要必要的宽度 不强制换行
内联元素例子
<span>
<a>

改变元素显示
可以更改内联元素和区块元素
区块 -> 内联
li {
  display: inline;
}

内联 -> 区块
span {
  display: block;
}

Positioning(定位)
Static 定位
HTML元素的默认值，即没有定位，元素出现在正常的流中。
静态定位的元素不会受到top, bottom, left, right影响。

Fixed 定位
元素的位置相对于浏览器窗口是固定位置。
即使窗口是滚动的它也不会移动：

Relative 定位
相对定位元素的定位是相对其正常位置。

Absolute 定位
绝对定位的元素的位置相对于最近的已定位父元素，
如果元素没有已定位的父元素，那么它的位置相对于<html>:
Absolutely定位使元素的位置与文档流无关，因此不占据空间。
Absolutely定位的元素和其他元素重叠。

重叠的元素
元素的定位与文档流无关，所以它们可以覆盖页面上的其它元素
z-index属性指定了一个元素的堆叠顺序（哪个元素应该放在前面，或后面）
一个元素可以有正数或负数的堆叠顺序：
具有更高堆叠顺序的元素总是在较低的堆叠顺序元素的前面。

注意： 如果两个定位元素重叠，没有指定z-index，最后定位在HTML代码中的元素将被显示在最前面


元素怎样浮动
元素的水平方向浮动意味着元素只能左右移动而不能上下移动。
一个浮动元素会尽量向左或右。通常，这意味着尽所有的可能在所有包含元素的左侧或右侧的。
浮动元素之后的元素将围绕它。
浮动元素之前的元素将不会受到影响。

彼此相邻的浮动元素
如果你把几个浮动的元素放到一起，如果有空间的话，它们将彼此相邻

清除浮动 - 使用clear
元素浮动之后，周围的元素会重新排列，为了避免这种情况，使用clear属性
。clear属性指定其他元素双方都不能使用元素的浮动功能。
使用clear属性往文本中添加图片廊：

