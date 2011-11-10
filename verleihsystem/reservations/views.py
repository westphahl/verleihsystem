from datetime import date, timedelta

from django.conf import settings
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic.list import BaseListView
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


class ReservationDateListView(JSONResponseMixin, BaseListView):

    allow_empty = True

    def get_queryset(self):
        pid_list = self.request.POST.getlist('products[]')
        return Product.objects.filter(pk__in=pid_list).select_related('product_type')

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        self.object_list
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

        entry_list = ReservationEntry.objects.filter(
                product__in=self.object_list,
                reservation__state=1,
                reservation__end_date__gte=range_start,
                reservation__start_date__lte=range_end
            ).select_related('reservation')

        sorted_entries = dict()
        for entry in entry_list:
            try:
                sorted_entries[entry.product_id].append(entry)
            except KeyError:
                sorted_entries.update({ entry.product_id: [entry,]})

        context.update({
            'timeline': list(),
        })
        for product in self.object_list:
            current_date = range_start
            product.timeline = list()
            try:
                reservation_list = sorted_entries[product.id]
            except KeyError:
                reservation_list = list()

            while current_date < range_end:
                date_next = current_date + timedelta(days=1)
                reserved = [e for e in reservation_list if (
                    e.reservation.start_date <= current_date)
                    and (e.reservation.end_date >= current_date)]
                reserved_next = [e for e in reservation_list if (
                    e.reservation.start_date <= date_next)
                    and (e.reservation.end_date >= date_next)]
                product.timeline.append(
                    {'date': current_date, 'reserved': reserved, 'reserved_next': reserved_next})
                current_date += timedelta(days=1)

            html_context = {
                'product': product,
                'next_range': range_end,
                'previous_range': range_start - timedelta(days=day_range)
            }
            template = loader.get_template('products/snippet_timeline.html')
            html = template.render(RequestContext(self.request, html_context))

            context['timeline'].append((product.id, html))

        return context
