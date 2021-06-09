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
from first.generic_models import VignetteSubsession, VignettePlayer
import random

author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
First opinion collector
"""


class Constants(BaseConstants):
    name_in_url = 'prol'
    players_per_group = None
    num_rounds = 1
    bns = [False, True]

from django.core.validators import URLValidator
class Subsession(VignetteSubsession):
    def creating_session(self):
        super().creating_session()
        prolific_redirect_url = self.session.config.get('prolific_redirect_url')
        if not self.session.is_demo:
            URLValidator()(prolific_redirect_url)
            assert 'https://app.prolific.co/submissions' in prolific_redirect_url
        for p in self.get_players():
            p.order = random.choice(Constants.bns)

    def vignette(self):
        return dict(id=1)


class Group(BaseGroup):
    pass


class Player(VignettePlayer):
    timezone = models.StringField(blank=True)
    time_on_first_opinion = models.FloatField()