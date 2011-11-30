from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    mail = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)
