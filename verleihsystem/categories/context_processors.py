from categories.models import Category


def category_tree(request):
    """
    Context processor that adds all root categories to the template context.

    Template Context: tree_nodes => List of root categories
    """
    tree = Category.objects.root_nodes()
    return {'tree_nodes': tree}
