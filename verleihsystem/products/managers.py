from datetime import timedelta

from django.db import models


class ProductManager(models.Manager):
    """
    Custom manager for products. 
    """

    def with_timeline(self, product_list, start_date, end_date):
        from reservations.models import ReservationEntry
        """
        Returns the list of products of a queryset with an extra 'timeline'
        attribute.
        
        - The timeline contains only acknowledged and requested reservations.
        - The timeline is a list containing a dict for each day in the given
          time frame which has a 'date' and 'state' key.
        - 'date' is a Python date object
        - 'state' is a list of reserveration states for the day (if any)
        """
        # Get list of products and possible reservations
        entry_list = ReservationEntry.objects.filter(
                product__in=product_list,
                reservation__state__in=[0, 1],
                reservation__end_date__gte=start_date,
                reservation__start_date__lte=end_date
            ).select_related('reservation')

        # Group reservations by product id
        sorted_entries = dict()
        for entry in entry_list:
            try:
                sorted_entries[entry.product_id].append(entry)
            except KeyError:
                sorted_entries.update({ entry.product_id: [entry,]})

        # Create product timelines
        for product in product_list:
            current_date = start_date
            product.timeline = list()
            try:
                reservation_list = sorted_entries[product.id]
            except KeyError:
                reservation_list = list()

            while current_date < end_date:
                state = [e.reservation.state for e in reservation_list if (
                    e.reservation.start_date <= current_date)
                    and (e.reservation.end_date >= current_date)]
                product.timeline.append(
                    {'date': current_date, 'state': state})
                current_date += timedelta(days=1)

        return product_list

    def with_timeline_for_type(self, product_type, start_date, end_date):
        """
        Returns a list of products with an extra 'timeline' attribute.
        
        Products are filtered by product type.
        """
        product_list = self.get_query_set().filter(product_type=product_type
            ).select_related('product_type')
        return self.with_timeline(product_list, start_date, end_date)

    def with_timeline_for_pids(self, pid_list, start_date, end_date):
        """
        Returns a list of products with an extra 'timeline' attribute.
        
        Products are filtered by pid_list.
        """
        product_list = self.get_query_set().filter(id__in=pid_list
            ).select_related('product_type')
        return self.with_timeline(product_list, start_date, end_date)
