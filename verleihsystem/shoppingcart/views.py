from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from products.models import Product

def index(request):
    try:
        request.session['cart']
    except KeyError:
        request.session['cart'] = []
    return render_to_response("shoppingcart/index.html",
        context_instance=RequestContext(request))

def clear(request):
    try:
        del request.session['cart']
    except KeyError:
        pass
    return redirect('/cart/')

def add(request):
    try:
        request.session['cart']
    except KeyError:
        request.session['cart'] = []
    pid = request.GET.get('id', '0')
    obj = get_object_or_404(Product, id=pid)
    if obj not in request.session['cart']:
        request.session['cart'].append(obj)
    request.session.modified = True
    return redirect('/cart/')

def remove(request):
    pid = request.GET.get('id', '0')
    obj = get_object_or_404(Product, id=pid)
    if obj in request.session['cart']:
        request.session['cart'].remove(obj)
    request.session.modified = True
    return redirect('/cart/')
