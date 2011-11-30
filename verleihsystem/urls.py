from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'categories.views.index', name='home'),
    url(r'^contact/$', 'contact.views.contact_form', name='contact_form'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^category/', include('categories.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^cart/', include('shoppingcart.urls')),
    url(r'^reservations/', include('reservations.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
