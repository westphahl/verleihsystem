from django import forms
from mptt.forms import TreeNodeMultipleChoiceField

from products.models import ProductType
from categories.models import Category


class ProducttypeAdminForm(forms.ModelForm):
    """
    Admin form for a product type.

    Changes the categories field in the Django admin to display a multiple
    choice field with the categories formatted as a tree.
    """
    categories = TreeNodeMultipleChoiceField(queryset=Category.tree.all())

    class Meta:
        model = ProductType
