from django.conf.urls.defaults import patterns, url

from shoppingcart.views import ShoppingCartIndexView

urlpatterns = patterns('shoppingcart.views',
    url(r'^$', ShoppingCartIndexView.as_view(), name='shoppingcart_index'),
    url(r'^add/$', 'add_product', name='shoppingcart_add'),
    url(r'^remove/$', 'remove_product', name='shoppingcart_remove'),
    url(r'^clear/$', 'clear_shoppingcart', name='shoppingcart_clear'),
)
