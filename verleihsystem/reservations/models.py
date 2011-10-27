from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from products.models import Product


class Reservation(models.Model):
    STATE_CHOICES = (
        (0, _("Pending")),
        (1, _("Acknowledged")),
        (2, _("Rejected")),
    )
    user = models.ForeignKey(User, verbose_name=_("User"))
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))
    timestamp = models.DateField(verbose_name=_("Timestamp"),
            auto_now_add=True)
    state = models.IntegerField(verbose_name=_("State"), default=0,
            choices=STATE_CHOICES,)
    comments = models.TextField(blank=True, verbose_name=_("Comments"))

    def __unicode__(self):
        return u"%s: %s - %s" % (self.user, self.start_date, self.end_date)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        get_latest_by = 'timestamp'
        ordering = ['end_date']


class ReservationEntry(models.Model):
    reservation = models.ForeignKey(Reservation, verbose_name=_("Reservation"))
    product = models.ForeignKey(Product, verbose_name=_("Product"))

    def clean(self):
        collision = ReservationEntry.objects.filter(product=self.product,
                reservation__start_date__gte=self.reservation.start_date,
                reservation__end_date__lte=self.reservation.end_date)
        if len(collision) > 0:
            raise ValidationError(_("There is already a reservation for this product."))
    
    def __unicode__(self):
        return u"%s | %s" % (self.reservation, self.product)

    class Meta:
        verbose_name = _("Reservation Entry")
        verbose_name_plural = _("Reservation Entries")