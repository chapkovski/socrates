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
        "phil_background",
        "stats_background",
        "stem_background",
        "critical_background",
        "country_born",
        "country_life",
        "survey_experience",
        "other_comments",
    ]


page_sequence = [Q]
