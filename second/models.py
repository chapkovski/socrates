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


class Constants(BaseConstants):
    name_in_url = 't'
    players_per_group = 2
    num_rounds = 1
    seconds_to_chat = 10  # TODO: do we need this? this limits them now to stay a min time on chat page.
    sec_to_wait_on_wp = 10  # this limits the time they stay on the wp without a partner before being redirected further
    seconds_allow_exit =  10  # After how many seconds they allwered to leave the chat. TODO: move to session settings
    msg_till_allowed_exit = 'Time till you are allowed to finish the chat'
    matching_choices = [Match.NOT_YET, Match.NOT_MATCHED,
                        Match.MATCHED]  # -1 means is not matched yet, 0 - no partners found, 1 - means matched.


class Subsession(VignetteSubsession):
    def group_by_arrival_time_method(self, waiting_players):
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

            for i in waiting_players:
                pos = i.participant.vars.get('position')
                rest = [j for j in waiting_players if j.participant.vars.get('position') != pos]
                if rest:
                    group = [i, rest[0]]
                    for p in group:
                        p.matched = Match.MATCHED
                    return group

    def creating_session(self):
        super().creating_session()
        first_exists = 'first' in self.session.config.get('app_sequence')
        if first_exists:
            for p in self.get_players():
                p.order = p.participant.first_player.first().order
        else:
            for p in self.get_players():
                p.order = random.choice(FirstConstants.bns)


class Group(BaseGroup):
    time_allow_exit = djmodels.DateTimeField(blank=True, null=True)

    def set_timer(self):
        self.time_allow_exit = datetime.now(timezone.utc) + relativedelta(seconds=Constants.seconds_allow_exit)

    @property
    def seconds_till_allow_to_leave(self):
        return (self.time_allow_exit - datetime.now(timezone.utc)).total_seconds()

    def time_to_chat_over(self):
        if self.time_chat_end:
            return (self.time_chat_end - datetime.now(timezone.utc)).total_seconds() * 1000

    def chat(self, id_in_group, payload, **kwargs):
        text = payload.get('text', )
        if text:
            p = self.get_player_by_id(id_in_group)
            ch = Chat.objects.create(owner=p, group=self, body=text)
            others = self.player_set.exclude(id=p.id).values_list('id_in_group', flat=True)
            to_others = {i: dict(text=text, action='incomingMessage') for i in others}
            resp = {p.id_in_group: dict(text=f'ECHO: {ch.body}', source=id_in_group + 1, action='confirm'),
                    **to_others}
            return resp
        request_old_messages = payload.get('request_old_messages', False)
        if request_old_messages:
            msgs = self.chats.all().order_by('id')
            msgs = [{'text': i.body, 'source': i.owner.id_in_group} for i in msgs]
            return {id_in_group: dict(msgs=msgs, action='PrevMessages')}
        decision = payload.get('decision', False)
        if decision:
            print('DECISION!', decision, id_in_group)


class Player(VignettePlayer):
    wp_entrance_time = djmodels.DateTimeField(null=True, blank=True)
    wp_exit_time = djmodels.DateTimeField(null=True, blank=True)
    wp_waiting_time = djmodels.DurationField(null=True, blank=True)
    matched = models.IntegerField(blank=True, choices=Constants.matching_choices, initial=Match.NOT_YET)

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
