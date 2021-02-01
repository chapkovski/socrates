from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,

)
from datetime import datetime, timedelta, timezone
from django.db import models as djmodels

from first.generic_models import VignetteSubsession, VignettePlayer
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)
author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
Second opinion collector + chat
"""

import random
from first.models import Constants as FirstConstants
from enum import IntEnum


class Match(IntEnum):
    NOT_YET = -1
    NOT_MATCHED = 0
    MATCHED = 1


def independent_payoff(g, p):
    correct = p.subsession.correct
    answer = p.answer
    fee = p.subsession.fee_for_correct
    return fee * (answer == correct)


def dependent_payoff(g, p):
    correct = p.subsession.correct
    fee = p.subsession.fee_for_correct
    all_correct = all([i.answer == correct for i in g.get_players()])
    return fee * all_correct


class Constants(BaseConstants):
    name_in_url = 't'
    players_per_group = 2
    num_rounds = 1
    seconds_to_chat = 10  # TODO: do we need this? this limits them now to stay a min time on chat page.
    sec_to_wait_on_wp = 10  # this limits the time they stay on the wp without a partner before being redirected further

    matching_choices = [Match.NOT_YET, Match.NOT_MATCHED,
                        Match.MATCHED]  # -1 means is not matched yet, 0 - no partners found, 1 - means matched.

    payoff_funs = dict(
        no_reward=lambda x,y: 0,
        solo_reasoning=independent_payoff,
        dependent=dependent_payoff,
        independent=independent_payoff
    )

class Subsession(VignetteSubsession):
    seconds_allow_exit = models.IntegerField()
    msg_till_allowed_exit = models.StringField()
    seconds_forced_exit = models.IntegerField()
    msg_forced_exit = models.StringField()
    fee_for_correct = models.CurrencyField()
    def group_by_arrival_time_method(self, waiting_players):
        if not self.session.config.get('chat'):
            return [waiting_players[0]]
        now = datetime.now(timezone.utc)
        waited_too_long = [p for p in waiting_players if now > p.wp_exit_time]
        for p in waited_too_long:
            p.matched = Match.NOT_MATCHED

            return [p]
        # this for debuginng only (when 'first' is not in app chain)
        if 'first' not in self.session.config.get('app_sequence') and len(waiting_players) > 1:
            group = waiting_players[:2]
            for p in group:
                p.matched = Match.MATCHED
            return group
        if len(waiting_players) > 1:
            return waiting_players[:2]

    def creating_session(self):
        super().creating_session()
        assert Constants.payoff_funs.get(self.session.config.get('param_name')), 'No payoff function found!'
        self.seconds_allow_exit = self.session.config.get('seconds_allow_exit')
        self.msg_till_allowed_exit = self.session.config.get('msg_till_allowed_exit')
        self.seconds_forced_exit = self.session.config.get('seconds_forced_exit')
        self.msg_forced_exit = self.session.config.get('msg_forced_exit')  # 'This chat will end in'
        self.fee_for_correct = self.session.config.get('fee_for_correct')  # How much they earn for correct answer?

        first_exists = 'first' in self.session.config.get('app_sequence')
        if first_exists:
            for p in self.get_players():
                p.order = p.participant.first_player.first().order
        else:
            for p in self.get_players():
                p.order = random.choice(FirstConstants.bns)

class Group(BaseGroup):
    time_allow_exit = djmodels.DateTimeField(blank=True, null=True)
    time_forced_exit = djmodels.DateTimeField(blank=True, null=True)
    chat_status = models.BooleanField()

    def set_payoffs(self):
        payoff_fun = Constants.payoff_funs.get(self.session.config.get('param_name'))
        if not payoff_fun:
            logger.error('No payoff function is found! Check for correct param_name')
            return
        for p in self.get_players():
            p.payoff = payoff_fun(self, p)

    def set_timer(self):
        self.chat_status = True
        self.time_allow_exit = datetime.now(timezone.utc) + relativedelta(
            seconds=self.subsession.seconds_allow_exit)
        self.time_forced_exit = datetime.now(timezone.utc) + relativedelta(
            seconds=self.subsession.seconds_forced_exit)

    @property
    def seconds_till_allow_to_leave(self):
        return (self.time_allow_exit - datetime.now(timezone.utc)).total_seconds()

    def time_to_chat_over(self):
        return (self.time_forced_exit - datetime.now(timezone.utc)).total_seconds()

    def chat(self, id_in_group, payload, **kwargs):
        if payload.get('participant_left_chat'):
            self.chat_status = False
            return {0: dict(participant_left_chat=True, action='endOfChat')}
        text = payload.get('text')
        if text:
            p = self.get_player_by_id(id_in_group)
            ch = Chat.objects.create(owner=p, group=self, body=text)
            others = self.player_set.exclude(id=p.id).values_list('id_in_group', flat=True)
            to_others = {i: dict(text=text, action='incomingMessage') for i in others}
            resp = {p.id_in_group: dict(text=f'ECHO: {ch.body}', source=id_in_group + 1, action='confirm'),
                    **to_others}
            return resp
        request_old_messages = payload.get('request_old_messages')
        if request_old_messages:
            msgs = self.chats.all().order_by('id')
            msgs = [{'text': i.body, 'source': i.owner.id_in_group} for i in msgs]
            return {id_in_group: dict(msgs=msgs, action='PrevMessages', chatStatus=self.chat_status)}

class Player(VignettePlayer):
    wp_entrance_time = djmodels.DateTimeField(null=True, blank=True)
    wp_exit_time = djmodels.DateTimeField(null=True, blank=True)
    wp_waiting_time = djmodels.DurationField(null=True, blank=True)
    matched = models.IntegerField(blank=True, choices=Constants.matching_choices, initial=Match.NOT_YET)
    essay = models.LongStringField()

    def get_instructions(self):
        """
         Return instructions here based on treatment type
        """
        return self.session.config.get('param_name')

    def checking_matching(self):
        too_late = datetime.now(timezone.utc) > self.wp_exit_time
        if too_late:
            self.matched = int(too_late)
        return self.matched

class Chat(djmodels.Model):
    body = models.StringField()
    owner = djmodels.ForeignKey(to=Player, related_name='chats', on_delete=djmodels.CASCADE)
    group = djmodels.ForeignKey(to=Group, related_name='chats', on_delete=djmodels.CASCADE)

class Vignette(djmodels.Model):
    title = djmodels.CharField(unique=True, max_length=100)
    body = models.LongStringField()
    question = models.StringField()
    yes_option = models.StringField()
    no_option = models.StringField()
    correct = models.BooleanField()
