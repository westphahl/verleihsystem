from django.conf.urls.defaults import patterns, url
from products.views import ProductTypeDetailView


urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', ProductTypeDetailView.as_view(),
        name='product_type_detail'),
)
