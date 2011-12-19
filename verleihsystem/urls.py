from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^contact/$', 'contact.views.contact_form', name='contact_form'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^category/', include('categories.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^cart/', include('shoppingcart.urls')),
    url(r'^reservations/', include('reservations.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
