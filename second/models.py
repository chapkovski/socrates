from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,

)
import os
from otree.models import Participant
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, timezone
from django.db import models as djmodels

from first.generic_models import VignetteSubsession, VignettePlayer
from dateutil.relativedelta import relativedelta
import logging
from itertools import cycle

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


# TODO: move to classes all this BS.

def independent_payoff(g, p):
    correct = p.subsession.correct
    answer = p.answer
    fee = p.subsession.fee_for_correct
    return dict(payoff=fee * (answer == correct),
                ego_correct=answer == correct,
                )


def dependent_payoff(g, p):
    answer = p.answer
    alter_answer = p.other.answer
    correct = p.subsession.correct
    fee = p.subsession.fee_for_correct
    all_correct = all([i.answer == correct for i in g.get_players()])
    return dict(payoff=fee * all_correct,
                ego_correct=answer == correct,
                alter_correct=alter_answer == correct,
                both_correct=all_correct)


def no_reward(g, p):
    correct = p.subsession.correct
    answer = p.answer
    return dict(payoff=0,
                ego_correct=answer == correct)


class Constants(BaseConstants):
    name_in_url = 't'
    answer_correspondence = {False: 'no_option',
                             True: 'yes_option'}
    CHAT_TREATMENTS = ['dependent', 'independent']
    NO_CHAT_TREATMENTS = ['no_reward', 'solo_reasoning']
    players_per_group = 2
    num_rounds = 1
    sec_waiting_too_long = 15
    seconds_to_chat = 10  # TODO: do we need this? this limits them now to stay a min time on chat page.
    sec_to_wait_on_wp = 10  # this limits the time they stay on the wp without a partner before being redirected further


    matching_choices = [Match.NOT_YET, Match.NOT_MATCHED,
                        Match.MATCHED]  # -1 means is not matched yet, 0 - no partners found, 1 - means matched.

    payoff_funs = dict(
        no_reward=no_reward,
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

    @property
    def dependable_treatment(self):
        return self.session.config.get('param_name') == 'dependent'

    def group_by_arrival_time_method(self, waiting_players):
        """
        If there are those who wait too long, we just assign them to a no_reward treatment and let them proceed.
        Otherwise we match them with the opposite views
        """
        if not self.session.config.get('chat'):
            return [waiting_players[0]]
        now = datetime.now(timezone.utc)
        neg_holders = [w for w in waiting_players if
                       not w.participant.vars.get('position') and type(w.participant.vars.get('position')) is bool]
        pos_holders = [w for w in waiting_players if
                       w.participant.vars.get('position') is True]
        bot_session = waiting_players[0].participant._is_bot
        too_long_waiters = []
        if bot_session:
            if len(waiting_players) > 1:
                shortl, longl, = sorted([pos_holders, neg_holders], key=lambda x: len(x))
                too_long_waiters = longl[len(shortl):]
            else:
                for i in waiting_players:
                    i.participant.vars.setdefault('attempt_counter', 0)
                    i.participant.vars['attempt_counter'] += 1
                    if i.participant.vars['attempt_counter'] > 9:
                        i.treatment = random.choice(Constants.NO_CHAT_TREATMENTS)
                        return [i]
        else:
            too_long_waiters = [w for w in waiting_players if
                                (now - w.wp_entrance_time).total_seconds() > w.sec_waiting_too_long]
        if too_long_waiters:
            for i in too_long_waiters:
                i.treatment = random.choice(Constants.NO_CHAT_TREATMENTS)
                return [too_long_waiters[0]]

        if len(waiting_players) > 1:
            if neg_holders and pos_holders:
                return [neg_holders[0], pos_holders[0]]

    def creating_session(self):
        super().creating_session()
        assert Constants.payoff_funs.get(self.session.config.get('param_name')), 'No payoff function found!'
        p = self.get_players()[0]

        path_to_instructions = 'data/instructions/'
        with os.scandir(path_to_instructions) as entries:
            for entry in entries:
                html_ext = '.html'
                if entry.name.endswith(html_ext):
                    filename = entry.name[:-len(html_ext)]
                    with open(f'{path_to_instructions}{filename}.html') as reader:
                        Param.objects.get_or_create(name=filename, defaults=dict(body=reader.read()))
        param_name = self.session.config.get('param_name')
        try:
            Param.objects.get(name=param_name)
        except (Param.DoesNotExist):
            raise Exception(
                'Something wrong with instructions parameters. Check for their existance or ask Philipp what to do')
        self.seconds_allow_exit = self.session.config.get('seconds_allow_exit')
        self.msg_till_allowed_exit = self.session.config.get('msg_till_allowed_exit')
        self.seconds_forced_exit = self.session.config.get('seconds_forced_exit')
        self.msg_forced_exit = self.session.config.get('msg_forced_exit')  # 'This chat will end in'
        self.fee_for_correct = self.session.config.get('fee_for_correct')  # How much they earn for correct answer?
        for p in self.get_players():
            p.treatment = param_name
        first_exists = 'first' in self.session.config.get('app_sequence')
        if first_exists:
            for p in self.get_players():
                p.order = p.participant.first_player.first().order
        else:
            potanswers = cycle([False, True])
            for p in self.get_players():
                if self.session.is_demo:  ## only for debugging!!
                    p.participant.vars['position'] = next(potanswers)
                p.order = random.choice(FirstConstants.bns)


class Group(BaseGroup):
    time_allow_exit = djmodels.DateTimeField(blank=True, null=True)
    time_forced_exit = djmodels.DateTimeField(blank=True, null=True)
    chat_status = models.BooleanField()

    def set_payoffs_and_results(self):
        param_name = self.get_players()[0].treatment
        payoff_fun = Constants.payoff_funs.get(param_name)
        if not payoff_fun:
            logger.error('No payoff function is found! Check for correct param_name')
            return
        for p in self.get_players():
            p.set_payoff()
            response = payoff_fun(self, p)
            p.payoff = response.get('payoff')
            p.participant.vars.update(response)

    def when_matched(self, ):
        for p in self.get_players():
            p.matched = Match.MATCHED
        self.chat_status = self.session.config.get('chat')

    def set_timer(self, ):

        # We set the allowed time to exit both for essays and chats because we
        # don't let people the essay as well
        self.time_allow_exit = datetime.now(timezone.utc) + relativedelta(
            seconds=self.subsession.seconds_allow_exit)
        # for the sake of simplicity (and Jesus Christ) we keep forced_exit option on exit although
        # it is not enforced
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


def original_answer(player):
    pos = player.participant.vars.get('position')
    return getattr(player.subsession, Constants.answer_correspondence.get(pos))


class Player(VignettePlayer):
    @property
    def original_ego_answer(self):
        return original_answer(self)

    @property
    def original_alter_answer(self):
        alter = self.get_others_in_group()[0]
        return original_answer(alter)

    @property
    def sec_waiting_too_long(self):
        return self.session.config.get('sec_waiting_too_long', Constants.sec_waiting_too_long)

    def set_payoff(self):
        param_name = self.treatment
        payoff_fun = Constants.payoff_funs.get(param_name)
        if not payoff_fun:
            logger.error('No payoff function is found! Check for correct param_name')
            return

        response = payoff_fun(self.group, self)
        self.payoff = response.get('payoff')
        self.participant.vars.update(response)


    wp_entrance_time = djmodels.DateTimeField(null=True, blank=True)
    wp_exit_time = djmodels.DateTimeField(null=True, blank=True)
    wp_waiting_time = djmodels.DurationField(null=True, blank=True)
    matched = models.IntegerField(blank=True, choices=Constants.matching_choices, initial=Match.NOT_YET)
    essay = models.LongStringField()
    time_on_comprehension_check = models.FloatField()
    time_on_discussion = models.FloatField()
    time_on_essay = models.FloatField()
    time_on_second_opinion = models.FloatField()
    treatment = models.StringField()

    @property
    def other(self):
        return self.get_others_in_group()[0]

    @property
    def in_chat_treatment(self):
        return self.treatment in Constants.CHAT_TREATMENTS

    def get_instructions(self):
        """
         Return instructions here based on treatment type.
         TODO: use render_to_string to inject some variables (like fee for correct answer)
        """

        return mark_safe(Param.objects.get(name=self.treatment).body)

    def checking_matching(self):
        too_late = datetime.now(timezone.utc) > self.wp_exit_time
        if too_late:
            self.matched = int(too_late)
        return self.matched


class Chat(djmodels.Model):
    body = models.StringField()
    timestamp = djmodels.DateTimeField(auto_now_add=True)
    owner = djmodels.ForeignKey(to=Player, related_name='chats', on_delete=djmodels.CASCADE)
    group = djmodels.ForeignKey(to=Group, related_name='chats', on_delete=djmodels.CASCADE)


class Vignette(djmodels.Model):
    title = djmodels.CharField(unique=True, max_length=100)
    body = models.LongStringField()
    question = models.StringField()
    yes_option = models.StringField()
    no_option = models.StringField()
    correct = models.BooleanField()


class Param(djmodels.Model):
    name = models.StringField(unique=True)
    body = models.LongStringField()


class TimeTracker(djmodels.Model):
    class Meta:
        unique_together = ['owner', 'page', 'period', 'app_name']

    owner = djmodels.ForeignKey(to=Participant,
                                on_delete=djmodels.CASCADE,
                                related_name='timetrackers')
    page = models.StringField()
    period = models.IntegerField()
    get_time = djmodels.DateTimeField()
    post_time = djmodels.DateTimeField(null=True)
    seconds_on_page = models.IntegerField()
    app_name = models.StringField()


def custom_export(players):
    yield ['session', 'participant_code', 'target_code', 'timestamp', 'text', 'group_id', ]
    for p in Chat.objects.all():
        yield [p.owner.session.code,
               p.owner.participant.code,
               p.owner.get_others_in_group()[0].participant.code,
               p.timestamp,
               p.body,
               p.group.id_in_subsession,
               ]
