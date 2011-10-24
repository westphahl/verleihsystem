from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


def get_photo_path(instance, filename):
    upload_dir = 'accounts/'
    path, ext = filename.split('.')
    return upload_dir + instance.user.username + '.' + ext


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

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")
