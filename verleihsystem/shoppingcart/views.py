from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.views.generic.base import TemplateView
from django.http import Http404
from django.conf import settings
from django.core.urlresolvers import reverse

from products.models import Product
from reservations.models import ReservationEntry


class ShoppingCartIndexView(TemplateView):

    template_name = 'shoppingcart/index.html'

    def get_context_data(self, **kwargs):
        # Call implementation in base class to get context
        context = super(ShoppingCartIndexView, self).get_context_data(**kwargs)

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

        context.update({
            'next_range': range_end,
            'previous_range': range_start - timedelta(days=day_range),
        })

        try:
            pid_list = self.request.session['cart']
        except KeyError:
            pid_list = []

        product_list = Product.objects.filter(id__in=pid_list
            ).select_related('product_type')
        entry_list = ReservationEntry.objects.filter(
                product__in=product_list,
                reservation__end_date__gte=range_start,
                reservation__start_date__lte=range_end
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
                state = [e.reservation.state for e in reservation_list if (
                    e.reservation.start_date <= current_date)
                    and (e.reservation.end_date >= current_date)]
                product.timeline.append(
                    {'date': current_date, 'state': state})
                current_date += timedelta(days=1)

        context.update({
            'product_list': product_list,
        })
        return context


def clear_shoppingcart(request):
    try:
        del request.session['cart']
    except KeyError:
        pass
    return redirect(reverse('shoppingcart_index'))


@require_GET
def add_product(request):
    try:
        pid = int(request.GET.get('id', None))
        request.session['cart']
    except KeyError:
        request.session['cart'] = []
    except (TypeError, ValueError):
        raise Http404

    product = get_object_or_404(Product, id=pid)

    if product.id not in request.session['cart']:
        request.session['cart'].append(product.id)
        request.session.modified = True
    return redirect(reverse('shoppingcart_index'))


@require_GET
def remove_product(request):
    try:
        request.session['cart']
        pid = int(request.GET.get('id', None))
    except KeyError:
        request.session['cart'] = []
    except (TypeError, ValueError):
        raise Http404

    if pid in request.session['cart']:
        request.session['cart'].remove(pid)
        request.session.modified = True
    return redirect(reverse('shoppingcart_index'))
