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
from .generic_models import VignetteSubsession, VignettePlayer
import random

author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
First opinion collector
"""


class Constants(BaseConstants):
    name_in_url = 'first'
    players_per_group = None
    num_rounds = 1
    bns = [False, True]


class Subsession(VignetteSubsession):
    def creating_session(self):
        super().creating_session()
        for p in self.get_players():
            p.order = random.choice(Constants.bns)

    def vignette(self):
        return dict(id=1)


class Group(BaseGroup):
    pass


class Player(VignettePlayer):
    timezone = models.StringField(blank=True)
    time_on_first_opinion = models.FloatField()