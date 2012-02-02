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
