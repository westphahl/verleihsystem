from django.utils.translation import ugettext as _
from django.db.models import Count
from django.contrib import admin

from products.models import ProductType, Product
from products.forms import ProducttypeAdminForm


class ProductInline(admin.TabularInline):
    """
    Inline for editing products on the product type admin page.
    """
    model = Product
    extra = 0


class ProductTypeAdmin(admin.ModelAdmin):
    """
    Admin for the product type model.

    Uses a modified admin form so that the categorie tree is formatted in a
    more user friendly way.
    In the admin list view it displays the number of associated products.
    """
    form = ProducttypeAdminForm
    list_filter = ('categories',)
    list_display = ('name', 'product_count',)
    prepopulated_fields = {'slug': ['name',]}
    search_fields = ['name',]
    inlines = [
        ProductInline,
    ]

    def queryset(self, request):
        """
        Returns the queryset for the admin list view after adding the number
        of associated products.
        """
        qs = super(ProductTypeAdmin, self).queryset(request)
        return qs.annotate(Count('product'))

    def product_count(self, obj):
        """
        Returns the formatted field of the product count for display in the
        admin list view.
        """
        return u"%s" %(obj.product__count)
    product_count.short_description = _("Number of products")


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product)
