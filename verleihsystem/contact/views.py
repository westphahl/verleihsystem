from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

from contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = ['info@example.com']
            
            if cc_myself:
                recipients.append(sender)
            redirect(reverse('home'))
    else:
        form = ContactForm()
    
    return render_to_response('contact.html', {'form': form,}, 
            context_instance=RequestContext(request))
