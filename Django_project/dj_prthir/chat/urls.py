#encoding:utf-8

from django.conf.urls import patterns, include, url
from chat import views

urlpatterns = patterns('',
  url(r'^$',    views.dashboard, name="dashboard"),
  url(r'^send_msg/', views.send_msg, name="chat_send_msg"),
  url(r'^get_msg/', views.get_msg, name="get_new_msg"),
)
