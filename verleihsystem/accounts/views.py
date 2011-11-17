from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from accounts.forms import UserProfileForm
from accounts.models import UserProfile


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

def dashboard(request):
    return render_to_response('accounts/dashboard.html', 
        context_instance=RequestContext(request))
