from django.conf.urls import include, url
from django.contrib import admin

#from dj_prtwo import views
import web

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_prtwo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^web/', include('web.urls')),
]
