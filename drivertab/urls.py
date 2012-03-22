# coding=utf-8

from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'drivertab.iodata.views.login'),
    (r'^logout/', 'drivertab.iodata.views.logout'),
    (r'^trips/$', 'drivertab.iodata.views.trips'),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
