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
from datetime import datetime, timedelta, timezone
from django.db import models as djmodels
from operator import itemgetter
from first.generic_models import VignetteSubsession, VignettePlayer
import random

author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
Second opinion collector + chat
"""

import random
from first.models import Constants as FirstConstants


class Constants(BaseConstants):
    name_in_url = 't'
    players_per_group = 2
    num_rounds = 1
    seconds_to_chat = 10  # TODO: do we need this? this limits them now to stay a min time on chat page.
    sec_to_wait_on_wp = 20  # this limits the time they stay on the wp without a partner before being redirected further


class Subsession(VignetteSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        for i in waiting_players:
            print('WWWW', datetime.now(timezone.utc) - i.wp_entrance_time)
        # TODO matching conditions go here for pairing conflicting views
        if len(waiting_players) > 1:
            for i in waiting_players:
                i.matched = True
            return waiting_players[:2]

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
    time_chat_start = djmodels.DateTimeField(blank=True, null=True)
    time_chat_end = djmodels.DateTimeField(blank=True, null=True)

    def set_timer(self):
        self.time_chat_start = datetime.utcnow()
        self.time_chat_end = self.time_chat_start + timedelta(seconds=Constants.seconds_to_chat)

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
    wp_waiting_time = djmodels.DurationField(null=True, blank=True)
    matched = models.BooleanField(blank=True)

    def checking_matching(self):
        self.wp_waiting_time = datetime.now(timezone.utc) - self.wp_entrance_time
        if self.wp_waiting_time.total_seconds() > Constants.sec_to_wait_on_wp:
            self.matched = False


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
