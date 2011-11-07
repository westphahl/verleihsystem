from django.conf.urls.defaults import patterns, url
from reservations.views import ReservationDateListView


urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<pk>\d+)/$',
        ReservationDateListView.as_view(),
        name='reservation_date_list'),
)
