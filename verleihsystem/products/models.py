from django.db import models
from django.utils.translation import ugettext as _

from categories.models import Category


class ProductType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    picture = models.ImageField(blank=True, upload_to='products',
        verbose_name=_("Photo"))

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = _("Product type")
        verbose_name_plural = _("Product types")


class Product(models.Model):
    product_type = models.ForeignKey(ProductType)
    sn = models.CharField(max_length=255, verbose_name=_("Serial/Id"))
    brief_description = models.TextField(verbose_name=_("Brief description"),
        blank=True)

    def __unicode__(self):
        return u"%s" % (self.sn)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
