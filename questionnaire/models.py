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
from django_countries.fields import CountryField
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
    age = models.IntegerField(label='How old are you?')
    sex = models.IntegerField(label='What is your gender?', choices=[(0,'Female'),(1,'Male'), (2, 'Other'), (3,'Prefer not to answer')])
    race = models.IntegerField(label='What is your race', choices=[(0, 'White'), (1, 'Black'), (2, 'Other')])
    education = models.IntegerField(label='What is the highest educational level you have attained?', choices=[(0, 'BA'), (1, 'MA'), (2, 'Ph.D')])
    ses = models.IntegerField()
    philosophy = models.IntegerField()
    stats = models.IntegerField()
    stem = models.BooleanField()
    critical = models.BooleanField()
    country_born = CountryField(null=True, blank=True)
    country_life = models.StringField()
    experience = models.IntegerField()
    comment = models.LongStringField()
