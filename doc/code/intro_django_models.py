from django.db import models

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    add_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
	return self.title
