from django.forms import ModelForm


class DependentFieldForm(ModelForm):
    dependent_fields = None

    class Media:
        js = ('js/limit_dependent_fields.js',)

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
                        is_valid = False
        return is_valid
