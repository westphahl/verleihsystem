class ProductTypeDetailView(DetailView):

    model = ProductType

    def get_context_data(self, **kwargs):
        context = super(ProductTypeDetailView, self).get_context_data(**kwargs)

        timeline = self.request.GET.get('timeline', None)
        range_start = date.today()
        try:
            if timeline:
                year, month, day = map(int, timeline.split('-'))
                range_start = date(year, month, day)
        except ValueError:
            pass

        day_range = getattr(settings, 'RESERVATION_TIMELINE_RANGE', 14)
        range_end = range_start + timedelta(days=day_range)

        context.update({
            'next_range': range_end,
            'previous_range': range_start - timedelta(days=day_range),
        })

        product_list = Product.objects.with_timeline_for_type(
            self.object, range_start, range_end)

        context.update({
            'product_list': product_list,
        })
        return context
