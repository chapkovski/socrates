from otree.api import Currency as c, currency_range
from ._builtin import WaitPage, Page
from django.shortcuts import redirect
from .models import Constants


class Results(Page):
    pass


class FinalForProlific(Page):
    def is_displayed(self):
        return self.session.config.get('for_prolific')

    def get(self):
        return redirect(self.session.config.get('prolific_redirect_url'))


page_sequence = [
    Results,
    FinalForProlific
]
