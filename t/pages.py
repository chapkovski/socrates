from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstWP(WaitPage):
    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'


class DiscussionPage(Page):
    live_method = 'chat'
    form_model = 'player'
    form_fields = ['answer', 'confidence']


page_sequence = [
    FirstWP,
    DiscussionPage, ]
