class ReservationEntry(models.Model):
    reservation = models.ForeignKey(Reservation, verbose_name=_("Reservation"))
    product = models.ForeignKey(Product, verbose_name=_("Product"))
