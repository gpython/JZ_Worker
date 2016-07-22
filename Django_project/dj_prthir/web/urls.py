#encoding:utf-8

from django.conf.urls import patterns, include, url
from web import views

urlpatterns = patterns('',
  #{ }
  url(r'^$',                            views.index, name="index"),
  url(r'logout/',                       views.dj_logout, name="logout"),
  url(r'login/',                        views.dj_login, name="login"),
  url(r'reg/',                          views.dj_reg, name='reg'),
  url(r'list/(\d*)/',                   views.list, name="list"),
  url(r'new/',                          views.new_article, name="new_article"),
  url(r'category/(\d+)/',               views.category, name="category"),
  url(r'article_detail/(\d+)/',         views.article_detail, name="article_detail"),
)
