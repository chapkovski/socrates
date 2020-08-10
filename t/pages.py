from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstWP(WaitPage):
    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'

class DiscussionPage(Page):
    live_method = 'chat'
    def post(self):

        return super().post()

page_sequence = [
    FirstWP,
    DiscussionPage, ]
