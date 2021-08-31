from first.generic_pages import GeneralVignettePage
from ._builtin import Page
import humanize
from django.shortcuts import redirect
from first.forms import CQForm


class BlockingWarning(Page):
    def is_displayed(self):
        return self.session.config.get('blocking')


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

    def vars_for_template(self):
        if self.player.cq_err_counter == 0:
            return dict(attempts_left=False)
        max_attempts = self.player.session.config.get('blocking_attempts', 3)
        attempts_left = max_attempts - self.player.cq_err_counter
        return dict(attempts_left=attempts_left+1)

    def get_form_class(self):
        return CQForm


class Blocked(Page):
    def is_displayed(self):
        max_attempts = self.player.session.config.get('blocking_attempts', 3)
        return self.player.cq_err_counter >= max_attempts

    def post(self):
        """That's just a cheap way to block those who still will try to submit."""
        return redirect(self.request.path)


page_sequence = [
    BlockingWarning,
    PreIntro,
    Intro,
    Opinion,
    PreInstructions,
    ComprehensionCheck,
    Blocked
]
