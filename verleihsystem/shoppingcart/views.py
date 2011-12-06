from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.views.generic.edit import FormView
from django.http import Http404
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from products.models import Product
from reservations.models import Reservation, ReservationEntry
from shoppingcart.forms import ShoppingCartReservationFormset


class ShoppingCartIndexView(FormView):
    """
    View for displaying and processing the shopping cart.
    """

    template_name = 'shoppingcart/index.html'
    form_class = ShoppingCartReservationFormset
    # reverse() doesn't work here. This is fixed in Django 1.4
    # See: https://code.djangoproject.com/ticket/5925
    success_url = '/reservations/'

    def post(self, request, *args, **kwargs):
        """
        Process a POST request.
        """
        form_class = self.get_form_class()
        formset = self.get_form(form_class)
        if formset.is_valid() and self.process_formset(formset):
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    @transaction.commit_manually
    def process_formset(self, formset):
        """
        Process the formset of the shopping cart.

        All interaction with the database is wrapped in a transaction. If there
        is an error while processing the formset the whole transaction is
        rolled back and no reservations are created.
        """
        commit = True
        user=self.request.user
        pid_list = self.request.session.get('cart')
        if not pid_list:
            return False
        product_list = Product.objects.filter(id__in=pid_list)

        # Create a reservation for every timeframe and reservation entries
        # for all the products.
        for form in formset:
            start_date=form.cleaned_data.get('start_date')
            end_date=form.cleaned_data.get('end_date')
            # Empty form; process next
            if not (start_date and end_date):
                continue

            try:
                reservation = Reservation(user=user, start_date=start_date,
                        end_date=end_date)
                reservation.clean()
                reservation.save()
                for product in product_list:
                    # Make sure there is no resevation entry for the product
                    # in the given timeframe.
                    # We can't use the models clean() method here since we
                    # are inside a transaction.
                    collision = ReservationEntry.objects.filter(
                        product=product, reservation__state=1).exclude(
                        reservation__end_date__lt=start_date).exclude(
                        reservation__start_date__gt=end_date).count()
                    if collision > 0:
                        raise ValidationError(
                            _("There is already a reservation for %s "
                              "product in this timeframe.") % product)
                    e = ReservationEntry(reservation=reservation, product=product)
                    e.save()
            except ValidationError, e:
                # Add the error message to the form, so that we can display
                # the error to the user.
                form.invalidate_form(e.messages)
                commit = False
        if commit:
            transaction.commit()
            del self.request.session['cart']
        else:
            transaction.rollback()
        return commit

    def get_context_data(self, **kwargs):
        """
        Returns the context for the shopping cart.

        Adds the products with corresponding timelines to the template context.
        """
        # Call implementation in base class to get context
        context = super(ShoppingCartIndexView, self).get_context_data(**kwargs)

        range_start = date.today()
        # Fallback if client has no AJAX/JS support
        try:
            timeline = self.request.GET.get('timeline', None)
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

        # Get product ids from session
        try:
            pid_list = self.request.session['cart']
        except KeyError:
            pid_list = []

        # Get list of producs and possible reservations
        product_list = Product.objects.filter(id__in=pid_list
            ).select_related('product_type')
        entry_list = ReservationEntry.objects.filter(
                product__in=product_list,
                reservation__end_date__gte=range_start,
                reservation__start_date__lte=range_end
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
    """
    Clears the shopping cart.
    """
    try:
        del request.session['cart']
    except KeyError:
        pass
    return redirect(reverse('shoppingcart_index'))


@require_GET
def add_product(request):
    """
    Adds a product to the shopping cart.
    """
    try:
        pid = int(request.GET.get('id', None))
        request.session['cart']
    except KeyError:
        # Empty shopping cart
        request.session['cart'] = []
    except (TypeError, ValueError):
        # Invalid product id
        raise Http404

    # Make sure we've got a valid product id
    product = get_object_or_404(Product, id=pid)

    # Add product to shopping cart
    if product.id not in request.session['cart']:
        request.session['cart'].append(product.id)
        request.session.modified = True
    return redirect(reverse('shoppingcart_index'))


@require_GET
def remove_product(request):
    """
    Removes a product from the shopping cart.
    """
    try:
        request.session['cart']
        pid = int(request.GET.get('id', None))
    except KeyError:
        # Empty shopping cart
        request.session['cart'] = []
    except (TypeError, ValueError):
        # Invalid product id
        raise Http404

    # Remove product from shopping cart
    if pid in request.session['cart']:
        request.session['cart'].remove(pid)
        request.session.modified = True
    return redirect(reverse('shoppingcart_index'))
