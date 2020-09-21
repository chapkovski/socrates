from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from datetime import datetime, timedelta, timezone


class FirstWP(WaitPage):
    def is_displayed(self):
        if not self.player.wp_entrance_time:
            self.player.wp_entrance_time = datetime.now(timezone.utc)
        self.player.checking_matching()
        return self.player.matched is None  # is it reliable enough?

    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'


class DiscussionPage(Page):
    live_method = 'chat'
    form_model = 'player'
    form_fields = ['answer', 'confidence']

    def is_displayed(self):
        return self.player.matched


class NoMatchingPage(Page):
    def is_displayed(self):
        return not self.player.matched


page_sequence = [
    FirstWP,
    DiscussionPage,
    NoMatchingPage,
]
