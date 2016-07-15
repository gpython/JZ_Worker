#encoding:utf-8
from django.conf.urls import include, url
from django.contrib import admin

from dj_prone import views
import web
import ad


urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_prone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),

    url(r'^list/(?P<item>\d*)/(?P<id>\d*)/$', views.list),
    url(r'^list/(?P<item>\d*)/$', views.list, {'id':1000}),

    url(r'^web/', include('web.urls')),
#    url(r'^ad/', include('ad.urls')),


]
