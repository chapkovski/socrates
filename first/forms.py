from django import forms
import random
from .models import Constants


class CQForm(forms.Form):

    def __init__(self, *args, **kwargs):
        view = kwargs.pop('view')
        kwargs.pop('instance')
        self.player = view.player
        super().__init__(*args, **kwargs)
        cqs = Constants.cqs.copy()
        # random.shuffle(cqs)
        for i in cqs:
            self.fields[i.get('name')] = forms.BooleanField(required=False,
                                                            label=i.get('label'),
                                                            widget=forms.CheckboxInput())

    def save(self):
        pass

    def clean(self):
        cleaned_data = super().clean()
        all_correct = True
        max_attempts = self.player.session.config.get('blocking_attempts', 3)
        if self.player.cq_err_counter >= max_attempts:
            return
        for i in Constants.cqs:

            if bool(int(i.get('correct'))) != cleaned_data.get(i.get('name')):
                curval = getattr(self.player, f'{i.get("name")}_err_counter')
                setattr(self.player, f'{i.get("name")}_err_counter', curval + 1)
                all_correct = False
                self.player.save()
        if not all_correct:
            self.player.cq_err_counter += 1
            self.player.save()
            raise forms.ValidationError('Some answers are incorrect. Please read instructions and try once again.')
