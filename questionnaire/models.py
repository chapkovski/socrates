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

author = 'Philip Chapkovski, HSE-Moscow'

doc = """
Post-experimental questionnaire for Socrates projet
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='')
    sex = models.IntegerField()
    race = models.IntegerField()
    education = models.IntegerField()
    ses = models.IntegerField()
    philosophy = models.IntegerField()
    stats = models.IntegerField()
    stem = models.BooleanField()
    critical = models.BooleanField()
    country_born = models.StringField()
    country_life = models.StringField()
    experience = models.IntegerField()
    comment = models.LongStringField()
