from datetime import date, timedelta

from django.conf import settings
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.utils import simplejson as json
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from reservations.models import Reservation, ReservationEntry
from products.models import Product


@login_required
def dashboard(request, template='accounts/dashboard.html', *args, **kwargs):
    """
    Displays a dashboard view with all the reservations of the current user.
    """
    today = date.today()
    reservation_list = Reservation.objects.filter(user=request.user).exclude(
        end_date__lte=today, return_date__lte=today)

    # Sort reservations
    overdue = []
    borrowed = []
    reserved = []
    requested = []
    rejected = []
    for reservation in reservation_list:
        if reservation.state == 0:
            # Reservation was requested and is not yet approved
            requested.append(reservation)
        elif reservation.state == 2:
            # Reservation was rejected
            rejected.append(reservation)
        elif (reservation.end_date < today) and not reservation.return_date:
            # Reservation is overdue
            overdue.append(reservation)
        elif reservation.borrow_date:
            # Reservations was fetched
            borrowed.append(reservation)
        else:
            # Reservation is approved
            reserved.append(reservation)

    reservation_categories = [
        [_("Overdue"), overdue],
        [_("Borrowed"), borrowed],
        [_("Reserved"), reserved],
        [_("Requested"), requested],
        [_("Rejected"), rejected]
    ]
    return render_to_response(template,
        {'reservation_categories': reservation_categories},
        context_instance=RequestContext(request))


class ReservationDetailView(DetailView):
    """
    Detail view of a reservation along with the reserved products.
    """

    def get_queryset(self):
        """
        Filters the queryset by user and as a result prevents non-admin users
        from viewing unrelated reservations.
        """
        queryset = Reservation.objects.select_related()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class ReservationDeleteView(DeleteView):
    """
    Delete view for a reservation.
    """

    # reverse() doesn't work here. This is fixed in Django 1.4
    # See: https://code.djangoproject.com/ticket/5925
    success_url = '/user/dashboard/'

    def get_queryset(self):
        """
        Filters the queryset by user and as a result prevents non-admin users
        from deleting unrelated reservations.

        A reservation can only be deleted if it was not picked up yet.
        """
        queryset = Reservation.objects.filter(
            borrow_date__isnull=True).select_related()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class JSONResponseMixin(object):
    """
    View mixin for converting and returning the response as JSON.
    """

    def render_to_response(self, context):
        """Returns a JSON response containing context as payload."""
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        """Construct an HttpResponse object."""
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON."""
        return json.dumps(context)


class ReservationJSONDateList(JSONResponseMixin, BaseListView):
    """
    JSON timeline information for the requested products.
    """

    allow_empty = True

    def get_queryset(self):
        """
        Filters the queryset by requested products.
        """
        pid_list = self.request.POST.getlist('products[]')
        return Product.objects.filter(pk__in=pid_list).select_related('product_type')

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request.
        """
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Populates the context with the products and associated timelines. It
        also adds links for the next and previous timeline navigation.

        The range of the timelines is defined by the RESERVATION_TIMELINE_RANGE
        setting. (default: 14 days)
        """
        context = {}
        try:
            range_start = date(year=int(self.kwargs['year']),
                    month=int(self.kwargs['month']),
                    day=int(self.kwargs['day']))
        except ValueError:
            raise Http404

        day_range = getattr(settings, 'RESERVATION_TIMELINE_RANGE', 14)
        range_end = range_start + timedelta(days=day_range)

        next_args = range_end.isoformat().split('-')
        previous_args = (range_start - timedelta(days=day_range)).isoformat(
                ).split('-')

        next_url = reverse('reservation_date_list', args=next_args)
        previous_url = reverse('reservation_date_list', args=previous_args)

        context.update({
            'next_url': next_url,
            'previous_url': previous_url,
        })

        # Get product list with timeline attribute
        product_list = Product.objects.with_timeline(
            self.object_list, range_start, range_end)

        context.update({
            'timeline': list(),
        })
        for product in product_list:
            # Create context for timeline HTML snippet
            html_context = {
                'product': product,
                'next_range': range_end,
                'previous_range': range_start - timedelta(days=day_range)
            }
            template = loader.get_template('products/snippet_timeline.html')
            html = template.render(RequestContext(self.request, html_context))

            # Add HTML timeline for product
            context['timeline'].append((product.id, html))

        return context
