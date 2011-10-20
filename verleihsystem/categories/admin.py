from categories.models import Category
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'contact']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
