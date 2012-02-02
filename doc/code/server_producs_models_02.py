class Product(models.Model):
    product_type = models.ForeignKey(ProductType)
    sn = models.CharField(max_length=255, verbose_name=_(u"Serial/Id"))
    brief_description = models.TextField(verbose_name=_(u"Brief description"),
        blank=True)

    objects = ProductManager()
