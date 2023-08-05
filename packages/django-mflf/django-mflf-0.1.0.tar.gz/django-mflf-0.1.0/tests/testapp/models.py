from django.db import models

from model_field_list import ModelFieldListField


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    creation_date = models.DateField('creation date')
    color = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    weight = models.PositiveIntegerField()

    def __str__(self):
        return self.headline


class ProductGroup(models.Model):
    title = models.CharField(max_length=100)
    fields = ModelFieldListField('comparison fields', source_model=Product, blank=True)

    def __str__(self):
        return self.title
