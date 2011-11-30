from datetime import date

from django.contrib.auth.decorators import login_required
from reservations.models import Reservation


@login_required
def dashboard_info(request):
    today = date.today()
    overdue = Reservation.objects.filter(user=request.user,
        end_date__lt=today, return_date__isnull=True, state=1).exists()

    return {'dashboard_problem': overdue}
