from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.conf import settings

from contact.forms import ContactForm


def contact_form(request):
    """
    Displays and processes the email contact form.

    The email is sent to the recipient defined by the CONTACT_FORM_EMAIL
    setting. If the user is logged in, the form is populated with the user's
    name and email address.
    """
    if request.method == 'POST':
        # Process the form
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mail = form.cleaned_data['mail']
            subject = "[Verleihsystem:Kontakt]: " + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = [getattr(settings, 'CONTACT_FORM_EMAIL', '')]
            
            # CC the sender
            if cc_myself:
                recipients.append(mail)
            
            email = EmailMessage(subject=subject, body=message,
                to=recipients, headers={'Reply-To': mail})
            email.send()
            return redirect(reverse('home'))
    else:
        # Display the empty form
        if request.user.is_anonymous():
            form = ContactForm()
        else:
            name = "%s %s" % (request.user.first_name, request.user.last_name)
            mail = request.user.email
            form = ContactForm(initial={'name': name, 'mail': mail})
    
    return render_to_response('contact/contact_form.html', {'form': form,}, 
            context_instance=RequestContext(request))
