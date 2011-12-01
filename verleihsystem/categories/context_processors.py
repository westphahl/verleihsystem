from categories.models import Category


def category_tree(request):
    tree = Category.objects.root_nodes()
    
    return {'tree_nodes': tree}
