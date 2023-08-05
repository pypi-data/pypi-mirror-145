from django import forms
from django.core import checks, exceptions
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


class SeparatedValuesField(models.TextField):
    description = _("List stored as a string with separators")

    def __init__(self, verbose_name=None, name=None, separator=',', *args, **kwargs):
        self.separator = separator
        super(SeparatedValuesField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SeparatedValuesField, self).deconstruct()
        if self.separator is not None:
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, list):
            return value
        return value.split(self.separator)

    def from_db_value(self, value, expression, connection, *args):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.separator.join([s for s in value])

    def value_to_string(self, obj):
        value = self.value_from_obj(obj)
        return self.get_prep_value(value)


class ModelFieldListField(SeparatedValuesField):
    description = _("List of model fields")

    def __init__(self, verbose_name=None, name=None, source_model=None, *args, **kwargs):
        self.source_model = source_model
        if self.source_model:
            kwargs['choices'] = list(
                (field.name, capfirst(field.verbose_name)) if hasattr(field, 'verbose_name') else (field.name, capfirst(field.name))
                for field in self.source_model._meta.fields
                if field.db_column is None
            )
        super(ModelFieldListField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ModelFieldListField, self).deconstruct()
        del kwargs['choices']
        if self.source_model is not None:
            kwargs['source_model'] = self.source_model
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super(ModelFieldListField, self).check(**kwargs)
        errors.extend(self._check_source_model(**kwargs))
        return errors

    def _check_source_model(self, **kwargs):
        if not self.source_model:
            return [
                checks.Error(
                    "ModelFieldListFields must define 'source_model' attribute.",
                    obj=self,
                    id='modelfieldlistfields.E001',
                ),
            ]
        else:
            return []

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return
        if value not in self.empty_values:
            choices = set(map(lambda c: c[0], self.choices))
            if all(c in choices for c in value):
                return
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )
        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')
        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def formfield(self, **kwargs):
        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': self.get_choices(False)
        }
        defaults.update(kwargs)
        return forms.MultipleChoiceField(**defaults)


class ModelFieldListFormField(forms.MultipleChoiceField):
    def __init__(self, source_model=None, **kwargs):
        super(ModelFieldListFormField, self).__init__(**kwargs)
        self.source_model = source_model
        if self.source_model:
            self.choices = list(
                (field.name, capfirst(field.verbose_name)) if hasattr(field, 'verbose_name') else (field.name, capfirst(field.name))
                for field in self.source_model._meta.fields
                if field.db_column is None
            )
