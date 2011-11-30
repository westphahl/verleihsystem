from django.conf.urls.defaults import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from reservations.views import ReservationDetailView, ReservationDeleteView, \
    ReservationJSONDateList


urlpatterns = patterns('',
    url(r'^$', 'reservations.views.dashboard',
        name='reservation_dashboard'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        csrf_exempt(ReservationJSONDateList.as_view()),
        name='reservation_date_list'),
    url(r'detail/(?P<pk>\d+)/$',
        login_required(ReservationDetailView.as_view()),
        name='reservation_detail'),
    url(r'delete/(?P<pk>\d+)/$',
        login_required(ReservationDeleteView.as_view()),
        name='reservation_delete'),
)
