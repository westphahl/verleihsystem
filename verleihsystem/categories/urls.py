from django.conf.urls.defaults import patterns, url
from categories.views import category_detail

urlpatterns = patterns('',
    url(r'^(?P<path>(?:[\w-]+/)+)$', category_detail,
        {'template': 'categories/category_detail.html'},
        name='category_detail'),
)
