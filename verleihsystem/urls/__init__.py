from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^%s' % getattr(settings, 'SUB_URL', ''), include('urls.root')),
)
