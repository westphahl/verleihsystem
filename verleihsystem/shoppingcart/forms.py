from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _


class ShoppingCartReservationForm(forms.Form):
    date_formats = ('%d.%m.%Y',)
    start_date = forms.DateField(input_formats=date_formats)
    end_date = forms.DateField(input_formats=date_formats)

    def invalidate_form(self, messages):
        self._errors[NON_FIELD_ERRORS] = self.error_class(messages)

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            error_message = _(u"End date must be greater than or equal to "
                "the start date.")
            # We know that the 'end_date' field ist not in self._errors
            # since it exists in self.cleaned_data
            self._errors['end_date'] = self.error_class([error_message])
            del cleaned_data['end_date']

        return cleaned_data


ShoppingCartReservationFormset = formset_factory(ShoppingCartReservationForm)
