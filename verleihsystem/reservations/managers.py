from django.db import models


class ReservationEntryManager(models.Manager):
    """
    Custom manager for reservation entries. 
    """

    def get_query_set(self):
        return super(ReservationEntryManager, self).get_query_set(
            ).select_related('product')
