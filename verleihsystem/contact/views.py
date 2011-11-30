from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.conf import settings

from contact.forms import ContactForm


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mail = form.cleaned_data['mail']
            subject = "[Verleihsystem:Kontakt]: " + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = [getattr(settings, 'CONTACT_FORM_EMAIL', '')]
            
            if cc_myself:
                recipients.append(mail)
            
            email = EmailMessage(subject=subject, body=message,
                to=recipients, headers={'Reply-To': mail})
            email.send()
            return redirect(reverse('home'))
    else:
        if request.user.is_anonymous():
            form = ContactForm()
        else:
            name = request.user.first_name + " " + request.user.last_name
            mail = request.user.email
            form = ContactForm(initial={'name': name, 'mail': mail})
    
    return render_to_response('contact/contact_form.html', {'form': form,}, 
            context_instance=RequestContext(request))
