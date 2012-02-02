from django.template import Context, loader
from django.http import HttpResponse
from bookmarks.models import Bookmark

def list_bookmarks(request):
    bookmarks = Bookmark.objects.all()
    t = loader.get_template('bookmarks/list_view.html')
    c = Context({'bookmark_list': bookmarks})
    return HttpResponse(t.render(c))
