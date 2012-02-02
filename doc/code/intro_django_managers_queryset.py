$ ./manage.py shell
Python 2.7.2+ (default, Oct  4 2011, 20:06:09) 
[GCC 4.6.1] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> # Alle Lesezeichen abfragen
>>> from bookmarks.models import Bookmark
>>> Bookmark.objects.all()
[<Bookmark: Hochschule Ravensburg-Weingarten>]
>>> # Neues Lesezeichen anlegen und speichern
>>> b = Bookmark(title="Google", url="http://www.google.de/")
>>> b.save()
>>> Bookmark.objects.all()
[<Bookmark: Hochschule Ravensburg-Weingarten>, <Bookmark: Google>]
