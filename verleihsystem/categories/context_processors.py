from categories.models import Category


def category_tree(request):
    try:
        path = request.path
        path = path.split('/',2)
        leaf = Category.objects.get(path=path[2])
        
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
    except (Category.DoesNotExist, IndexError):
        tree = Category.objects.root_nodes()
    
    return {'tree_nodes': tree}
