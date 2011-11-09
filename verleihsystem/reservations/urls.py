from django.conf.urls.defaults import patterns, url
from django.views.decorators.csrf import csrf_exempt

from reservations.views import ReservationDateListView


urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        csrf_exempt(ReservationDateListView.as_view()),
        name='reservation_date_list'),
)
