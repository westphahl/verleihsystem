import mptt
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Category(MPTTModel):
    name = models.CharField(max_length=50)
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
