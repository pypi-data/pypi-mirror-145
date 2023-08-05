from django.test import TestCase
from django.contrib.admin.widgets import FilteredSelectMultiple

from testapp.forms import ProductExportForm


class MFLFFormTests(TestCase):
    def setUp(self):
        self.form = ProductExportForm({
            'export_fields': ['color', 'material']
        })

    def testFormData(self):
        self.assertTrue(self.form.is_valid())
        self.invalid_form = ProductExportForm({
            'export_fields': ['color', 'material', 'size']
        })
        self.assertFalse(self.invalid_form.is_valid())

    def testFormField(self):
        self.assertEqual(list(self.form.base_fields), ['export_fields'])
        self.assertEqual(type(self.form.base_fields['export_fields'].widget), FilteredSelectMultiple)
        self.assertEqual(self.form.base_fields['export_fields'].widget.choices, [
            ('id', 'ID'),
            ('title', 'Title'),
            ('description', 'Description'),
            ('price', 'Price'),
            ('creation_date', 'Creation date'),
            ('color', 'Color'),
            ('material', 'Material'),
            ('weight', 'Weight')
        ])

    def testFormWidget(self):
        self.assertInHTML('''
            <select name="export_fields" id="id_export_fields" required class="selectfilter"
             multiple data-field-name="product properties" data-is-stacked="0">
              <option value="id">ID</option>
              <option value="title">Title</option>
              <option value="description">Description</option>
              <option value="price">Price</option>
              <option value="creation_date">Creation date</option>
              <option value="color" selected>Color</option>
              <option value="material" selected>Material</option>
              <option value="weight">Weight</option>
            </select>
        ''', self.form.as_p())
