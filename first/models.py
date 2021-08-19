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
from csv import DictReader

author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
First opinion collector
"""


class Constants(BaseConstants):
    name_in_url = 'first'
    players_per_group = None
    num_rounds = 1
    bns = [False, True]
    with open("data/cqs.csv") as csvfile:
        cqs = list(DictReader(csvfile))


class Subsession(VignetteSubsession):
    def creating_session(self):
        super().creating_session()
        for p in self.get_players():
            p.order = random.choice(Constants.bns)
        for i in Constants.cqs:
            assert hasattr(p,
                           f"{i.get('name')}_err_counter"), f'Player class doesnt have corresponding counter for comprehension ' \
                                                            f"question {i.get('name')}"

    def vignette(self):
        return dict(id=1)


class Group(BaseGroup):
    pass


class Player(VignettePlayer):
    timezone = models.StringField(blank=True)
    time_on_first_opinion = models.FloatField()
    cq_err_counter = models.IntegerField(default=0, doc='Error counter for CQs')
    cq_1_err_counter = models.IntegerField(default=0, doc='Error counter for CQ1s')
    cq_2_err_counter = models.IntegerField(default=0, doc='Error counter for CQ2s')
    cq_3_err_counter = models.IntegerField(default=0, doc='Error counter for CQ3s')
    cq_4_err_counter = models.IntegerField(default=0, doc='Error counter for CQ4s')
    cq_5_err_counter = models.IntegerField(default=0, doc='Error counter for CQ5s')
    cq_6_err_counter = models.IntegerField(default=0, doc='Error counter for CQ6s')
