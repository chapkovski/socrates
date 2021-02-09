from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Q(Page):
    form_model = 'player'
    form_fields = [
        "age",
        "sex",
        "race",
        "education",
        "ses",
        "philosophy",
        "stats",
        "stem",
        "critical",
        "country_born",
        "country_life",
        "experience",
        "comment",
    ]


page_sequence = [Q]
