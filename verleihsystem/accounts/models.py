from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    student_number = models.PositiveIntegerField(blank=True, null=True,
        verbose_name=_("Student number"))
    phone = models.CharField(blank=True, max_length=100,
        verbose_name=_("Phone"))
    mobile_phone = models.CharField(blank=True, max_length=100,
        verbose_name=_("Mobile phone"))
    picture = models.ImageField(blank=True, upload_to='accounts',
        verbose_name=_("Photo"))

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")
