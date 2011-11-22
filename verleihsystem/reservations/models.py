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
    borrow_date = models.DateField(verbose_name=_("Borrow date"),
            blank=True, null=True)
    return_date = models.DateField(verbose_name=_("Return date"),
            blank=True, null=True)
    timestamp = models.DateField(verbose_name=_("Timestamp"),
            auto_now_add=True)
    state = models.IntegerField(verbose_name=_("State"), default=0,
            choices=STATE_CHOICES,)
    comments = models.TextField(blank=True, verbose_name=_("Comments"))

    def __unicode__(self):
        return u"%s: %s - %s" % (self.user, self.start_date, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        return ('reservation_detail', (), {'pk': self.id})

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(_("End date must be greater than start date."))

    def is_cancellable(self):
        return True if not self.borrow_date else False

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        get_latest_by = 'timestamp'
        ordering = ['end_date']


class ReservationEntry(models.Model):
    reservation = models.ForeignKey(Reservation, verbose_name=_("Reservation"))
    product = models.ForeignKey(Product, verbose_name=_("Product"))

    def clean(self):
        collision = ReservationEntry.objects.exclude(id=self.id).filter(
                product=self.product,
                reservation__state=1,
                reservation__end_date__gte=self.reservation.start_date,
                reservation__end_date__lte=self.reservation.end_date).count()
        if collision > 0:
            raise ValidationError(_("There is already a reservation for this "
                "product in the given timeframe."))
    
    def __unicode__(self):
        return u"%s | %s" % (self.reservation, self.product)

    class Meta:
        verbose_name = _("Reservation Entry")
        verbose_name_plural = _("Reservation Entries")
