from django import forms
from django.forms.formsets import formset_factory


class ShoppingCartReservationForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()


ShoppingCartReservationFormset = formset_factory(ShoppingCartReservationForm)
