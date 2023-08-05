from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.forms.widgets import SelectMultiple
from django.test import TestCase
from django.test.utils import override_settings

from testapp.models import ProductGroup


@override_settings(ROOT_URLCONF='testapp.urls_admin')
class MFLFAdminTests(TestCase):
    fixtures = ['tests']

    def setUp(self):
        site = AdminSite()
        self.admin = ModelAdmin(ProductGroup, site)

    def testForm(self):
        form_class = self.admin.get_form(None)
        form = form_class({'title': 'Spheres', 'fields': ['color', 'weight']}, instance=ProductGroup.objects.get(pk=1))
        self.assertTrue(form.is_valid())
        form = form_class({'title': 'Spheres', 'fields': ['color', 'size']}, instance=ProductGroup.objects.get(pk=2))
        self.assertFalse(form.is_valid())

    def testFieldListWidget(self):
        form = self.admin.get_form(None)
        self.assertEqual(list(form.base_fields), ['title', 'fields'])
        self.assertEqual(type(form.base_fields['fields'].widget), SelectMultiple)
        self.assertEqual(form.base_fields['fields'].widget.choices, [
            ('id', 'ID'),
            ('title', 'Title'),
            ('description', 'Description'),
            ('price', 'Price'),
            ('creation_date', 'Creation date'),
            ('color', 'Color'),
            ('material', 'Material'),
            ('weight', 'Weight')
        ])
