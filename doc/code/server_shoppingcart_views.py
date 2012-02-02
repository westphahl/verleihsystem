class ShoppingCartIndexView(FormView):
    [...]

    @transaction.commit_manually
    def process_formset(self, formset):
        commit = True
        user=self.request.user
        pid_list = self.request.session.get('cart')
        if not pid_list:
            return False
        product_list = Product.objects.filter(id__in=pid_list)

        for form in formset:
            start_date=form.cleaned_data.get('start_date')
            end_date=form.cleaned_data.get('end_date')
            if not (start_date and end_date):
                continue

            try:
                reservation = Reservation(user=user, start_date=start_date,
                        end_date=end_date)
                reservation.clean()
                reservation.save()
                for product in product_list:
                    collision = ReservationEntry.objects.filter(
                        product=product, reservation__state=1).exclude(
                        reservation__end_date__lt=start_date).exclude(
                        reservation__start_date__gt=end_date).count()
                    if collision > 0:
                        raise ValidationError(
                            _("There is already a reservation for %s "
                              "product in this timeframe.") % product)
                    e = ReservationEntry(reservation=reservation, 
                            product=product)
                    e.save()
            except ValidationError, e:
                form.invalidate_form(e.messages)
                commit = False
        if commit:
            transaction.commit()
            del self.request.session['cart']
        else:
            transaction.rollback()
        return commit
