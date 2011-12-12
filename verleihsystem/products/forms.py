from django import forms
from django.utils.translation import ugettext as _
from mptt.forms import TreeNodeMultipleChoiceField

from products.models import ProductType
from categories.models import Category


class ProducttypeAdminForm(forms.ModelForm):
    """
    Admin form for a product type.

    Changes the categories field in the Django admin to display a multiple
    choice field with the categories formatted as a tree.
    """
    categories = TreeNodeMultipleChoiceField(queryset=Category.tree.all(),
        label=_(u"Categories"))

    class Meta:
        model = ProductType
