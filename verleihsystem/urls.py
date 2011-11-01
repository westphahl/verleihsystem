from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'verleihsystem.views.home', name='home'),
    # url(r'^verleihsystem/', include('verleihsystem.foo.urls')),

    url(r'^$', 'categories.views.index'),
    url(r'^user/settings/$', 'accounts.views.settings'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^category/', include('categories.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
