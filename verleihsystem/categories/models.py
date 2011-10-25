from time import time

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    path = models.TextField(db_index=True, unique=True, blank=True)
    contact = models.ForeignKey(User, blank=True, null=True, 
        on_delete=models.SET_NULL, 
        limit_choices_to={'groups__name' : 'Verwalter'})
    parent = TreeForeignKey('self', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        # Make sure path field is not empty
        if self.path == '':
            self.path = str(self) + str(time())
        super(Category, self).save(*args, **kwargs)

        ancestors = self.get_ancestors()
        slugs = [a.slug for a in ancestors]
        slugs += [self.slug]
        self.path = '/'.join(slugs)
        super(Category, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('category_detail', (), {'path': self.path})
