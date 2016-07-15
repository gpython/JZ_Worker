#encoding:utf-8

from django.conf.urls import patterns, include, url
from web import views

urlpatterns = patterns('',
  url(r'index/', views.index),
  url(r'login/', views.login),
  url(r'ajax/', views.ajax),

)
