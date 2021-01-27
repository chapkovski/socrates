from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from first.generic_pages import GeneralVignettePage


class Opinion(GeneralVignettePage):


    live_method = 'decision_making'
    form_model = 'player'
    form_fields = ['answer', 'confidence', 'timezone']

    def is_displayed(self):
        return True

    def before_next_page(self):
        self.participant.vars['position'] = int(self.player.answer)


page_sequence = [Opinion]
