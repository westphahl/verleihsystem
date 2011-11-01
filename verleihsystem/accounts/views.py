from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.models import UserProfile

def settings(request):
    return render_to_response('accounts/settings.html',
        context_instance=RequestContext(request))
