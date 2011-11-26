from datetime import date

from django.template import RequestContext
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from reservations.models import Reservation

@login_required
def dashboard_info(request):
    today = date.today()
    reservation_list = Reservation.objects.filter(user=request.user).exclude(
        end_date__lte=today, return_date__lte=today)

    problem = False
    overdue = []
    for reservation in reservation_list:
        if (reservation.end_date < today) and not reservation.return_date:
            # Reservation is overdue
            overdue.append(reservation)
    if len(overdue) > 0:
        problem = True
    return {'dashboard_problem': problem}