from datetime import date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from reservations.models import Reservation


@login_required
def change_user_profile(request):
    try:
        user_profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        user_profile = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            if user_profile:
                profile.id = user_profile.id
            profile.user = request.user
            profile.save()

    else:
        form = UserProfileForm(instance=user_profile)
    return render_to_response('accounts/profile_form.html', {
        'formset': form,}, context_instance=RequestContext(request))


@login_required
def dashboard(request, template='accounts/dashboard.html', *args, **kwargs):
    today = date.today()
    reservation_list = Reservation.objects.filter(user=request.user).exclude(
        end_date__lte=today, return_date__lte=today)

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
