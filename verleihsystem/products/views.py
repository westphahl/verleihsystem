from django.views.generic.detail import DetailView
from products.models import ProductType, Product


class ProductTypeDetailView(DetailView):

    model = ProductType

    def get_context_data(self, **kwargs):
        # Call implementation in base class to get context
        context = super(ProductTypeDetailView, self).get_context_data(**kwargs)
        context.update({
            'product_list': Product.objects.filter(product_type=self.object),
        })
        return context

