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

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'first'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def vignette(self):
        return dict(id=1)


class Group(BaseGroup):
    def first_decision_making(self, id_in_group, payload, **kwargs):
        print(f'MESSAGE RECEIVED {payload} FROM: {id_in_group}')


class Player(BasePlayer):
    pass
