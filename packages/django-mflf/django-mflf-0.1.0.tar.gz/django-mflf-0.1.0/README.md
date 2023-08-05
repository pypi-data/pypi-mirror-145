# Django model field list field

[![Build Status](https://github.com/andreynovikov/django-mflf/workflows/Python%20package/badge.svg)](https://github.com/andreynovikov/django-mflf/actions?query=workflow%3A%22Python+package%22)
[![GitHub release](https://img.shields.io/github/release/andreynovikov/django-mflf.svg)](https://github.com/andreynovikov/django-mflf/releases/latest)
[![PyPI release](https://img.shields.io/pypi/v/django-mflf.svg)](https://pypi.org/project/django-mflf/)
[![Python version](https://img.shields.io/pypi/pyversions/django-mflf.svg)](https://pypi.org/project/django-mflf/)
[![GitHub issues](https://img.shields.io/github/issues/andreynovikov/django-mflf.svg)](https://github.com/andreynovikov/django-mflf/issues)
[![Codacy grade](https://img.shields.io/codacy/grade/2c886ef7ab034d44bd36c0e187f213d9)](https://www.codacy.com/gh/andreynovikov/django-mflf)
[![Codacy coverage](https://img.shields.io/codacy/coverage/2c886ef7ab034d44bd36c0e187f213d9)](https://www.codacy.com/app/novikov/django-mflf)
[![GitHub license](https://img.shields.io/github/license/andreynovikov/django-mflf.svg)](LICENSE)

This is a Django model field that provides a list of some other model's fields. Fields can be multi-selected and "under the hood" are stored as a comma-separated string. Also package provides simple form field with the same capabilities.

## Requirements

* Python 2.7+ or Python 3.3+
* Django 1.11+

## Installation

Install ```django-mflf``` using pip:

```shell
pip install django-mflf
```

Add ```model_field_list``` to ```INSTALLED_APPS```. Example:

```python
INSTALLED_APPS = (
    ...
    'model_field_list',
    ...
)
```

## Example usage

Model field:

```python
from model_field_list import ModelFieldListField

class ProductKind(models.Model):
    name = models.CharField(max_length=100)
    comparison = ModelFieldListField('comparison criteria', source_model=Product)
```

If referenced model has many fields it would be useful to use ```FilteredSelectMultiple``` in Django admin:

```python
from django.contrib.admin.widgets import FilteredSelectMultiple

class ProductKindAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            # different widget label is intentional
            'comparison': FilteredSelectMultiple('product properties', False)
        }
```

Simple form field:

```python
from django.contrib.admin.widgets import FilteredSelectMultiple
from model_field_list import ModelFieldListFormField

class ProductExportForm(ExportForm):
    export_fields = ModelFieldListFormField(source_model=Product, label='Export fields',
                                            widget=FilteredSelectMultiple('свойства товара', False))
```

## Limitations

- All model fields are listed, no option to filter them in any way.
- Field order can't be customized - they are sorted by the order of their definition in a model.
