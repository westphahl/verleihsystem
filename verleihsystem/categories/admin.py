from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from categories.models import Category


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'contact']
    prepopulated_fields = {"slug": ("name",)}
    exclude = ('path',)


admin.site.register(Category, CategoryAdmin)
