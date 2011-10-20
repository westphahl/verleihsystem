from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from categories.models import Category
from products.models import ProductType


def index(request):
    category_list = Category.tree.all()
    return render_to_response("home.html",
        {'nodes': category_list},
        context_instance=RequestContext(request))


def category_detail(request, path, template, *args, **kwargs):
    path = path.strip('/').split('/')
    leaf = get_object_or_404(Category, slug=path[-1])
    
    if len(path) > 1:
        path.pop()
        ancestors = leaf.get_ancestors()
        valid_path = [a.slug for a in ancestors]
        if valid_path != path:
            raise Http404

    sub_tree = leaf.get_descendants(include_self=True)
    product_list = ProductType.objects.filter(categories__in=sub_tree)
    return render_to_response(template, {'product_list': product_list, },
        context_instance=RequestContext(request))
