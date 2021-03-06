from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Count

from categories.models import Category
from products.models import ProductType


def category_detail(request, path, template, *args, **kwargs):
    """
    View for displaying a list product types of a category.
    """
    leaf = get_object_or_404(Category, path=path)

    # Build the tree for the category navigation
    tree = []
    tree.append(leaf)
    for c in leaf.get_children():
        tree.append(c)
    
    last_leaf = leaf
    for a in leaf.get_ancestors(True):
        tmp = []
        tmp.append(a)
        for cc in a.get_children():
            if last_leaf == cc:
                tmp.extend(tree)
                last_leaf = a;
            else:
                tmp.append(cc)
        tree = tmp
    
    tmp = []
    for r in last_leaf.get_siblings(True):
        if r == last_leaf:
            tmp.extend(tree)
        else:
            tmp.append(r)
    tree = tmp
    
    # Get all products for the current and its child categories
    sub_tree = leaf.get_descendants(include_self=True)
    product_list = ProductType.objects.filter(categories__in=sub_tree
        ).annotate(product_count=Count('product', distinct=True))
    return render_to_response(template, {'category': leaf, 'tree_nodes': tree,
        'product_list': product_list}, context_instance=RequestContext(request))
