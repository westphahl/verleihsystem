from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from shoppingcart.views import ShoppingCartIndexView


urlpatterns = patterns('shoppingcart.views',
    url(r'^$', login_required(ShoppingCartIndexView.as_view()),
        name='shoppingcart_index'),
    url(r'^add/$', 'add_product', name='shoppingcart_add'),
    url(r'^add/category/$', 'add_category', name='shoppingcart_add_category'),
    url(r'^remove/$', 'remove_product', name='shoppingcart_remove'),
    url(r'^clear/$', 'clear_shoppingcart', name='shoppingcart_clear'),
)
