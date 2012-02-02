class ProductType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_(u"Title"))
    slug = models.SlugField(max_length=50, help_text=_("A slug is a user-  
        and SEO-friendly short text used in a URL to identify and 
        describe a resource"))
    description = models.TextField(verbose_name=_(u"Description"), blank=True)
    categories = models.ManyToManyField(Category,
        verbose_name=_(u"Categories"))
    picture = models.ImageField(blank=True, upload_to=get_photo_path,
        verbose_name=_(u"Photo"))
