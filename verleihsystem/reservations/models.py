from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.contrib.sites.models import Site

from utils.path import get_media_path
from products.models import Product
from reservations.pdf import BorrowFormTemplate
from reservations.managers import ReservationEntryManager


class Reservation(models.Model):
    """
    Reservation of a user for a given timerange.
    """
    # Possible states of a reservation
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

    def __init__(self, *args, **kwargs):
        """
        Saves the current state for discovering changes.
        """
        super(Reservation, self).__init__(*args, **kwargs)
        self._previous_state = self.state

    def __unicode__(self):
        return u"%s: %s - %s" % (self.user, self.start_date, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the absolute path of a reservation.
        """
        return ('reservation_detail', (), {'pk': self.id})

    def clean(self):
        """
        Makes sure the timerange is valid.
        """
        if self.start_date > self.end_date:
            raise ValidationError(_("End date must be greater than start date."))

    def is_cancellable(self):
        """
        Checks whether the reservation can be cancelled. 
        """
        return True if not self.borrow_date else False

    def state_changed(self):
        """
        Checks if the state has changed.
        """
        if self.state != self._previous_state:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        """
        Generates the PDF form on save, if the reservation was acknowledged
        and notifies the user if the status has changed.
        """
        super(Reservation, self).save(*args, **kwargs)
        if self.state_changed():
            if self.state != 0:
                self.notify_user()
            if self.state == 1:
                self.create_pdf()

    def create_pdf(self):
        """
        Creates a PDF form for the reservation.
        """
        pdf_path = get_media_path(self.get_pdf_path())
        img_path = get_media_path('img/hrw_logo.png')
        pdf = BorrowFormTemplate(pdf_path, self, 4)
        pdf.set_logo(img_path, 42, 16)
        pdf.build()

    def notify_user(self):
        """
        Notify a user of a state change.
        """
        recipient = self.user.email
        if recipient != '':
            subject = u"[Verleihsystem] Reservierung %s" % (
                self.get_state_display().lower())
            reservation_url = u"http://%s%s" % (
                Site.objects.get_current().domain, self.get_absolute_url())

            # Render the message body
            template = loader.get_template('reservations/email_template.txt')
            message = template.render(
                    Context({'reservation': self, 'url': reservation_url}))

            # Create and send email
            email = EmailMessage(subject=subject, body=message, to=[recipient])
            email.send()

    def get_pdf_path(self):
        """
        Generates the path and name for the PDF form.
        """
        return 'reservations/%s_%s.pdf' % (self.user.username, str(self.id))

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        get_latest_by = 'timestamp'
        ordering = ['end_date']


class ReservationEntry(models.Model):
    """
    Entry for a specific product and reservation.
    """
    reservation = models.ForeignKey(Reservation, verbose_name=_("Reservation"))
    product = models.ForeignKey(Product, verbose_name=_("Product"))

    objects = ReservationEntryManager()

    def clean(self):
        """
        Makes sure there are no collisions with other reservations.
        """
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


class AdminReservationEntry(ReservationEntry):
    """
    Proxy model for allowing direct editing of reservation entries by admin
    users.
    """

    class Meta:
        proxy = True
        verbose_name = _("Reservation Entry")
        verbose_name_plural = _("Reservation Entries")
