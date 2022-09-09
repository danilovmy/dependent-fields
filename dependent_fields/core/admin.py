import json

from django.contrib import admin
from django.db.models import Q
from django.forms import ModelForm, ValidationError
from .models import Country, Region, Product


class DependentFieldForm(ModelForm):
    dependent_fields = None

    class Media:
        js = ('js/field_swapper.js',)

    def __init__(self, *args, **kwargs):
        self.set_dependent_fields(self.dependent_fields)
        super().__init__(*args, **kwargs)

    def set_dependent_fields(self, dependent_fields):
        if dependent_fields:
            for field_name, dependency in dependent_fields.items():
                field = self.base_fields.get(dependency, None)
                if field:  # check if dependent field is even in form
                    field.widget.attrs.update({
                        # add information about dependent fields into dataset of the widget
                        'data-dependent-fields': field.widget.attrs.get('data-dependent-fields', '') + 'id_' + field_name + ', ',
                        'onchange': field.widget.attrs.get('onchange', '') + 'limitDependentFields(this);'
                    })

    def is_valid(self, *args, **kwargs):
        is_valid = super().is_valid(*args, **kwargs)
        if is_valid and self.dependent_fields:
            for key, value in self.dependent_fields.items():
                if self.cleaned_data[key] and self.cleaned_data[value]:
                    relation_exists = type(self.cleaned_data[value]).objects.filter(**{'pk': self.cleaned_data[value].pk, key: self.cleaned_data[key].pk}).exists()
                    if not relation_exists:
                        # raise ValidationError('relation to depedent field does not exist')
                        is_valid = False
        return is_valid


class LimitSearchMixin:

    def get_search_results(self, request, qs, search_term):
        if request.GET.get('limit_choices_to'):
            qs = qs.complex_filter(json.loads(request.GET.get('limit_choices_to')))
        return super().get_search_results(request, qs, search_term)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Region)
class RegionAdmin(LimitSearchMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = DependentFieldForm
    dependent_fields = {'region': 'country'}
    list_display = ('name',)
    fields = ('name', 'country', 'region')
    autocomplete_fields = ('region', 'country')

    def get_form(self, *args, **kwargs):
        self.form.dependent_fields = self.dependent_fields
        return super().get_form(*args, **kwargs)
