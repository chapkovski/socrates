from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Opinion(Page):
    live_method = 'first_decision_making'
    form_model = 'player'
    form_fields = ['answer', 'confidence']



page_sequence = [Opinion]
