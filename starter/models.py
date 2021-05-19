from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.translation import gettext_lazy as _
from dateparser import parse
from dateutil.relativedelta import relativedelta
import humanize


def now():
    """
    Current UTC time wrapper
    :return: Current time in UTC timezone
    :rtype: datetime
    """
    return datetime.now(timezone('UTC'))


class Constants(BaseConstants):
    name_in_url = 'starter'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    time_to_start = djmodels.DateTimeField(blank=True, null=True)
    time_bonus = models.CurrencyField()
    time_to_proceed = models.IntegerField()
    delta = djmodels.DurationField(null=True, blank=True)
    formatted_delta = models.StringField()
    study_length = models.StringField()


    def creating_session(self):
        # in case there is no time to start in session config we fall back to current time plus 10 min
        self.time_bonus = self.session.config.get('time_bonus', 1)
        self.time_to_proceed = self.session.config.get('time_to_proceed', 10)
        self.delta = timedelta(seconds=self.time_to_proceed)
        self.formatted_delta = humanize.naturaldelta(self.delta)
        self.study_length = humanize.naturaldelta(self.session.config.get('study_length_min')*60)
        self.session.vars['study_length'] = self.study_length

        fallback_time = now() + relativedelta(seconds=10)
        fallback_time_str = str(fallback_time)
        time_to_start_str = self.session.config.get('time_to_start')

        if time_to_start_str in (None, 0, ''):
            time_to_start_str = fallback_time_str

        if time_to_start_str:
            time_to_start = parse(time_to_start_str)
            if not time_to_start.tzinfo:
                tz = timezone('UTC')
                time_to_start = tz.localize(time_to_start)

            if time_to_start < fallback_time:
                time_to_start = fallback_time
            self.time_to_start = time_to_start


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_times(self):
        self.time_to_pass = datetime.now(tz=timezone('UTC'))
        self.diff_to_pass = (self.time_to_pass - self.subsession.time_to_start).total_seconds()
        if not self.participant._is_bot:
            self.on_time = 0 < self.diff_to_pass < self.subsession.time_to_proceed
        else:
            self.on_time = True
        self.participant.vars['on_time'] = self.on_time

    arrival_time = djmodels.DateTimeField(blank=True, null=True)
    time_to_pass = djmodels.DateTimeField(blank=True, null=True)
    diff_to_pass = models.FloatField()
    worker_id = models.StringField()
    hit_id = models.StringField()
    assignment_id = models.StringField()
    on_time = models.BooleanField()
    consent = models.BooleanField(widget=widgets.CheckboxInput )

    def set_payoff(self):
        self.payoff = self.on_time * self.session.config.get('time_bonus', 0)
        self.participant.vars['bonus_time'] = self.payoff

    def start(self):
        self.arrival_time = now()
        self.worker_id = self.participant.vars.get('workerId')
        self.hit_id = self.participant.vars.get('hitId')
        self.assignment_id = self.participant.vars.get('assignmentId')
