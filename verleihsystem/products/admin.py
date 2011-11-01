from django.utils.translation import ugettext as _
from django.db.models import Count
from django.contrib import admin

from products.models import ProductType, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class ProductTypeAdmin(admin.ModelAdmin):
    list_filter = ('categories',)
    list_display = ('name', 'product_count',)
    filter_horizontal = ('categories',)
    prepopulated_fields = {'slug': ['name',]}
    search_fields = ['name',]
    inlines = [
        ProductInline,
    ]

    def queryset(self, request):
        qs = super(ProductTypeAdmin, self).queryset(request)
        return qs.annotate(Count('product'))

    def product_count(self, obj):
        return u"%s" %(obj.product__count)
    product_count.short_description = _("Number of products")


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product)
