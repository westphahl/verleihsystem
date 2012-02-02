from django.shortcuts import render_to_response
from bookmarks.models import Bookmark

def list_bookmarks(request):
    bookmarks = Bookmark.objects.all()
    return render_to_response(
        'bookmarks/list_view.html', {'bookmark_list': bookmarks})
