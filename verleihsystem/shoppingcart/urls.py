from django.conf.urls.defaults import patterns, url
from categories.views import category_detail

urlpatterns = patterns('',
    url(r'^$', 'shoppingcart.views.index'),
    url(r'^add/$', 'shoppingcart.views.add'),
    url(r'^remove/$', 'shoppingcart.views.remove'),
)
