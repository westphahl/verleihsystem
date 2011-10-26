from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from products.models import Product


class Reservation(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))
    timestamp = models.DateField(verbose_name=_("Timestamp"),
            auto_now_add=True)
    confirmed = models.BooleanField(verbose_name=_("Confirmed"))
    comments = models.TextField(blank=True, verbose_name=_("Comments"))

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        get_latest_by = 'timestamp'
        ordering = ['end_date']


class ReservationEntry(models.Model):
    reservation = models.ForeignKey(Reservation, verbose_name=_("Reservation"))
    product = models.ForeignKey(Product, verbose_name=_("Product"))
    
    class Meta:
        verbose_name = _("Reservation Entry")
        verbose_name_plural = _("Reservation Entries")
 
