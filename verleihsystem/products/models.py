import os
import hashlib
from time import time

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from categories.models import Category
from products.managers import ProductManager
from utils.image import scale_image


def get_photo_path(instance, filename):
    """
    Builds and returns the path where the product picture is saved.

    The returned filename contains a SHA1 hex digest to avoid any naming
    collisions.
    """
    upload_dir = 'products/'
    path, ext = filename.split('.')
    value = str(instance) + filename + str(time())
    hex_digest = hashlib.sha1(value).hexdigest()

    return upload_dir + hex_digest + '.' + ext


class ProductType(models.Model):
    """
    Product type for storing common product information.
    """
    name = models.CharField(max_length=50, verbose_name=_(u"Title"))
    slug = models.SlugField(max_length=50,
        help_text=_("A slug is a user- and SEO-friendly short text used in a "
            "URL to identify and describe a resource"))
    description = models.TextField(verbose_name=_(u"Description"), blank=True)
    categories = models.ManyToManyField(Category, verbose_name=_(u"Categories"))
    picture = models.ImageField(blank=True, upload_to=get_photo_path,
        verbose_name=_(u"Photo"))

    def __unicode__(self):
        return u"%s" % (self.name)

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the absolute path of a product type.
        """
        return ('product_type_detail', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        super(ProductType, self).save(*args, **kwargs)
        if self.picture and os.path.isfile(self.picture.path):
            width, height = getattr(settings, 'PRODUCT_IMAGE_SIZE', (200, 150))

            image = scale_image(self.picture.path, width, height)
            image.save(self.picture.path)

    class Meta:
        verbose_name = _(u"Product type")
        verbose_name_plural = _(u"Product types")


class Product(models.Model):
    """
    Concrete object of a product type.
    """
    product_type = models.ForeignKey(ProductType)
    sn = models.CharField(max_length=255, verbose_name=_(u"Serial/Id"))
    brief_description = models.TextField(verbose_name=_(u"Brief description"),
        blank=True)

    # Add custom manager
    objects = ProductManager()

    def __unicode__(self):
        return u"%s > %s" % (self.product_type, self.sn)

    class Meta:
        verbose_name = _(u"Product")
        verbose_name_plural = _(u"Products")
