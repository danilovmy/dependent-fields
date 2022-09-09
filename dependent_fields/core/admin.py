import json

from django.contrib import admin
from .models import Country, Region, Product
from .forms import DependentFieldForm

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
