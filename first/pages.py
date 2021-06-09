from first.generic_pages import GeneralVignettePage
from second.models import TimeTracker
from ._builtin import Page
import humanize


class PreIntro(Page):
    def vars_for_template(self):
        return dict(study_length=humanize.naturaldelta(self.session.config.get('study_length_min', 1) * 60))


class Intro(Page):
    pass


class Opinion(GeneralVignettePage):
    time_tracker_field = 'time_on_first_opinion'
    live_method = 'decision_making'
    form_model = 'player'
    form_fields = ['answer', 'confidence', 'timezone']

    def before_next_page(self):
        self.participant.vars['position'] = self.player.answer


page_sequence = [
    PreIntro,
    Intro,
    Opinion
]
