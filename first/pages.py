from first.generic_pages import GeneralVignettePage
from ._builtin import Page
import humanize

from first.forms import CQForm


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


class PreInstructions(Page):
    pass


class ComprehensionCheck(Page):
    time_tracker_field = 'time_on_comprehension_check'

    def get_form_class(self):
        return CQForm


page_sequence = [
    PreIntro,
    Intro,
    Opinion,
    PreInstructions,
    ComprehensionCheck,

]
