class Category(MPTTModel):
    CONTACT_GROUP = getattr(settings, 'CATEGORY_CONTACT_GROUP', 'Contact')

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    slug = models.SlugField(max_length=50, verbose_name=_("Slug"),
        help_text=_("A slug is a user- and SEO-friendly short text used in a "
            "URL to identify and describe a resource"))
    path = models.CharField(max_length=255, db_index=True, 
        unique=True, blank=True)
    contact = models.ForeignKey(User, blank=True, null=True, 
        on_delete=models.SET_NULL, verbose_name=_("Contact"),
        limit_choices_to={'groups__name' : CONTACT_GROUP})
    parent = TreeForeignKey('self', blank=True, null=True,
        verbose_name=_("Parent"))
