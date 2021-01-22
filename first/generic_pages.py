from ._builtin import Page


class GeneralVignettePage(Page):
    form_model = 'player'
    form_fields = ['answer', 'confidence']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if hasattr(self, 'form'):
            context['django_errors'] = self.form.errors.as_json() or {}
        return context
