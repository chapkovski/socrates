from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from datetime import datetime, timedelta


class FirstWP(WaitPage):
    def is_displayed(self):
        if not self.player.wp_entrance_time:
            self.player.wp_entrance_time = datetime.utcnow()
        return True

    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'


class DiscussionPage(Page):
    live_method = 'chat'
    form_model = 'player'
    form_fields = ['answer', 'confidence']


page_sequence = [
    FirstWP,
    DiscussionPage, ]
