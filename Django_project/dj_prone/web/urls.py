#encoding:utf-8

from django.conf.urls import patterns, include, url
from web import views

"""
urlpatterns = [
  url(r'^index/', views.index),
  url(r'^login/', views.login),
]
"""
"""
userspace = __import__('web.'+array[0])
model = getattr(userspace, array[0])
func = getattr(model, array[1])
func()
"""


urlpatterns = patterns('',
  url(r'^index/', views.index),
  url(r'^login/', views.login),
  url(r'add/(?P<name>\w*)/$', views.add),
  url(r'del/(?P<id>\d*)/$', views.dele),
  url(r'up/(?P<id>\d*)/(?P<hostname>\w*)/$', views.update),
  url(r'get/(?P<hostname>\w*)/$', views.gett),
  url(r'all/', views.all),
  url(r'reg/', views.Register),
)
