class ShoppingCartReservationForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def invalidate_form(self, messages):
        self._errors[NON_FIELD_ERRORS] = self.error_class(messages)

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            error_message = _(u"End date must be greater than or equal to "
                "the start date.")
            self._errors['end_date'] = self.error_class([error_message])
            del cleaned_data['end_date']

        return cleaned_data
