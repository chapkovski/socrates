from django import forms

from .models import Constants


class CQForm(forms.Form):

    def __init__(self, *args, **kwargs):
        view = kwargs.pop('view')
        kwargs.pop('instance')
        self.player = view.player
        super().__init__(*args, **kwargs)
        for i in Constants.cqs:
            self.fields[i.get('name')] = forms.BooleanField(required=False,
                                                            label=i.get('label'),
                                                            widget=forms.CheckboxInput())

    def save(self):
        pass

    def clean(self):
        cleaned_data = super().clean()
        if {i.get('name'): bool(int(i.get('correct'))) for i in Constants.cqs} != cleaned_data:
            self.player.cq_err_counter += 1
            self.player.save()
            raise forms.ValidationError('Some answers are incorrect. Please read instructions and try once again.')
