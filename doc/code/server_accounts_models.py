class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    student_number = models.PositiveIntegerField(blank=True, null=True,
        verbose_name=_("Student number"))
    phone = models.CharField(blank=True, max_length=100,
        verbose_name=_("Phone"))
    mobile_phone = models.CharField(blank=True, max_length=100,
        verbose_name=_("Mobile phone"))
    picture = models.ImageField(blank=True, upload_to=get_photo_path,
        verbose_name=_("Photo"))
