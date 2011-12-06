from datetime import date, timedelta

from django.conf import settings
from django.views.generic.detail import DetailView

from products.models import ProductType, Product


class ProductTypeDetailView(DetailView):
    """
    Detail view for a product type and its associated products.
    """

    model = ProductType

    def get_context_data(self, **kwargs):
        """
        Adds a list of all associated products and the corresponding product
        timelines to the template context. It also adds date objects for
        the next and previous timeline range.

        The range of the timelines is defined by the RESERVATION_TIMELINE_RANGE
        setting. (default: 14 days)
        """
        # Call implementation in base class to get context
        context = super(ProductTypeDetailView, self).get_context_data(**kwargs)

        timeline = self.request.GET.get('timeline', None)
        range_start = date.today()
        try:
            if timeline:
                year, month, day = map(int, timeline.split('-'))
                range_start = date(year, month, day)
        except ValueError:
            pass

        day_range = getattr(settings, 'RESERVATION_TIMELINE_RANGE', 14)
        range_end = range_start + timedelta(days=day_range)

        # Add date objects for next and previous timeline range
        context.update({
            'next_range': range_end,
            'previous_range': range_start - timedelta(days=day_range),
        })

        # Get product list with timeline attribute
        product_list = Product.objects.with_timeline_for_type(
            self.object, range_start, range_end)

        context.update({
            'product_list': product_list,
        })
        return context
