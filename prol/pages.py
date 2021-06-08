from first.generic_pages import GeneralVignettePage

from ._builtin import Page


class PreIntro(Page):
    pass


class Intro(Page):
    pass


class Opinion(GeneralVignettePage):
    time_tracker_field = 'time_on_first_opinion'
    live_method = 'decision_making'
    form_model = 'player'
    form_fields = ['answer', 'confidence', 'timezone']


from django.shortcuts import redirect





class Final(Page):
    def post(self):
        return redirect(self.session.config.get('prolific_redirect_url'))

page_sequence = [
    # PreIntro,
    Intro,
    Opinion,
    Final,
]
