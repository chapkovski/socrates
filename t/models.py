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
from datetime import datetime, timedelta,timezone
from django.db import models as djmodels
from operator import itemgetter

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 't'
    players_per_group = 2
    num_rounds = 1
    seconds_to_chat = 10


class Subsession(BaseSubsession):
    body = models.LongStringField()
    yes_option = models.LongStringField()
    no_option = models.LongStringField()
    vignette = djmodels.ForeignKey(to='Vignette', on_delete=djmodels.CASCADE, blank=True, null=True)

    def creating_session(self):
        vignette_title = self.session.config.get('vignette')
        if not vignette_title:
            raise Exception('Vignette title is necessary')
        try:
            v = Vignette.objects.get(title=vignette_title)
            self.vignette = v
            self.body = v.body
            self.yes_option = v.yes_option
            self.no_option = v.no_option
        except Vignette.DoesNotExist:
            raise Exception('Cannot find the vignette')

        for g in self.get_groups():
            for p in g.get_players():
                Chat.objects.create(group=g, owner=p, body=f'1st message from {p.id_in_group}')
                Chat.objects.create(group=g, owner=p, body=f'2st message from {p.id_in_group}')


class Group(BaseGroup):
    time_chat_start = djmodels.DateTimeField(blank=True, null=True)
    time_chat_end = djmodels.DateTimeField(blank=True, null=True)

    def set_timer(self):
        self.time_chat_start = datetime.now(timezone.utc)
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



class Player(BasePlayer):
    answer = models.BooleanField()

    def vignette_json(self):
        return dict(
            body=self.subsession.body,
            yes_option=self.subsession.yes_option,
            no_option=self.subsession.no_option,
        )


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
