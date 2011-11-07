from datetime import date, timedelta

from django.conf import settings
from django.views.generic.detail import DetailView

from products.models import ProductType, Product
from reservations.models import ReservationEntry


class ProductTypeDetailView(DetailView):

    model = ProductType

    def get_context_data(self, **kwargs):
        # Call implementation in base class to get context
        context = super(ProductTypeDetailView, self).get_context_data(**kwargs)
        product_list = Product.objects.filter(product_type=self.object)

        range_start = date.today()
        day_range = getattr(settings, 'RESERVATION_TIMELINE_RANGE', 14)
        range_end = range_start + timedelta(days=day_range)

        entry_list = ReservationEntry.objects.filter(
                product__in=product_list,
                reservation__state=1,
                reservation__end_date__gte=range_start,
                reservation__end_date__lt=range_end
            ).select_related('reservation')

        sorted_entries = dict()
        for entry in entry_list:
            try:
                sorted_entries[entry.product_id].append(entry)
            except KeyError:
                sorted_entries.update({ entry.product_id: [entry,]})

        for product in product_list:
            current_date = range_start
            product.timeline = list()
            try:
                reservation_list = sorted_entries[product.id]
            except KeyError:
                reservation_list = list()

            while current_date < range_end:
                reserved = [e for e in reservation_list if (
                    e.reservation.start_date <= current_date)
                    and (e.reservation.end_date >= current_date)]
                if reserved:
                    product.timeline.append(
                        {'date': current_date, 'reserved': True})
                else:
                    product.timeline.append(
                        {'date': current_date, 'reserved': False})
                current_date += timedelta(days=1)

        context.update({
            'product_list': product_list,
        })
        return context
