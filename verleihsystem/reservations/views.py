from datetime import date, timedelta

from django.conf import settings
from django.template import loader
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic.detail import BaseDetailView
from django.utils import simplejson as json

from reservations.models import ReservationEntry
from products.models import Product


class JSONResponseMixin(object):

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


class ReservationDateListView(JSONResponseMixin, BaseDetailView):

    model = Product

    def get_context_data(self, **kwargs):
        context = {'product': int(self.kwargs['pk']), 'timeline': list()}
        try:
            range_start = date(year=int(self.kwargs['year']),
                    month=int(self.kwargs['month']),
                    day=int(self.kwargs['day']))
        except ValueError:
            raise Http404

        day_range = getattr(settings, 'RESERVATION_TIMELINE_RANGE', 14)
        range_end = range_start + timedelta(days=day_range)

        next_args = range_end.isoformat().split('-') + [context['product'],]
        previous_args = (range_start - timedelta(days=day_range)).isoformat(
                ).split('-') + [context['product'],]

        next_url = reverse('reservation_date_list', args=next_args)
        previous_url = reverse('reservation_date_list', args=previous_args)

        context.update({
            'next_url': next_url,
            'previous_url': previous_url,
        })

        entries = ReservationEntry.objects.filter(
                product=int(self.kwargs['pk']),
                reservation__state=1,
                reservation__end_date__gte=range_start,
                reservation__start_date__lte=range_end)

        current_date = range_start

        while current_date < range_end:
            reserved = [e for e in entries if
                    (e.reservation.start_date <= current_date)
                    and (e.reservation.end_date >= current_date)]
            if reserved:
                context['timeline'].append(
                    {'date': (current_date.year,
                        current_date.month,
                        current_date.day),
                     'reserved': True})
            else:
                context['timeline'].append(
                    {'date': (current_date.year,
                        current_date.month,
                        current_date.day),
                     'reserved': False})
            current_date += timedelta(days=1)

        return context
