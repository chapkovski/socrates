from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from otree.common import _CurrencyEncoder
import json
from django.core.validators import URLValidator

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'last'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        prolific_redirect_url = self.session.config.get('prolific_redirect_url')
        if self.session.config.get('for_prolific'):
            URLValidator()(prolific_redirect_url)
            assert 'https://app.prolific.co/submissions' in prolific_redirect_url


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    vars_dump = models.LongStringField(doc='for storing participant vars')

    def start(self):
        self.vars_dump = json.dumps(self.participant.vars, cls=_CurrencyEncoder)
