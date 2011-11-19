from django import template
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Count

from categories.models import Category
from products.models import ProductType

def index(request):
    return render_to_response("home.html",
        context_instance=RequestContext(request))

def category_detail(request, path, template, *args, **kwargs):
    leaf = get_object_or_404(Category, path=path)
    
    sub_tree = leaf.get_descendants(include_self=True)
    product_list = ProductType.objects.filter(categories__in=sub_tree
        ).annotate(product_count=Count('product', distinct=True))
    return render_to_response(template, {'category': leaf,
        'product_list': product_list}, context_instance=RequestContext(request))
