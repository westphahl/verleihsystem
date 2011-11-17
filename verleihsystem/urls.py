from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'categories.views.index', name='home'),
    url(r'^user/profile/$', 'accounts.views.change_user_profile',
        name='user_profile_form'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^category/', include('categories.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^cart/', include('shoppingcart.urls')),
    url(r'^reservations/', include('reservations.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
