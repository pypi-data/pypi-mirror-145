from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from model_field_list import ModelFieldListFormField

from testapp.models import Product


class ProductExportForm(forms.Form):
    export_fields = ModelFieldListFormField(source_model=Product, widget=FilteredSelectMultiple('product properties', False))
