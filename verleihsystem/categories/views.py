from django.shortcuts import render_to_response
from categories.models import Category

def index(request):
    category_list = Category.tree.all()
    return render_to_response("home.html",
        {'nodes': category_list, 'request': request})
