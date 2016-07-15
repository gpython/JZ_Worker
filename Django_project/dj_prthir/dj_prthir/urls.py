from django.conf.urls import include, url
from django.contrib import admin

import web

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_prthir.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^web/', include('web.urls')),
]
