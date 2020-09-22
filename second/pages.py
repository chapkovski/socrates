from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from datetime import datetime, timedelta, timezone


class FirstWP(WaitPage):
    template_name = 'second/MatcherWP.html'

    def is_displayed(self):
        if not self.player.wp_entrance_time:
            self.player.wp_entrance_time = datetime.now(timezone.utc)
        if not self.player.wp_exit_time:
            self.player.wp_exit_time = datetime.now(timezone.utc) + timedelta(seconds=Constants.sec_to_wait_on_wp)
        self.player.checking_matching()
        return True  # TODO  self.player.matched is None  # is it reliable enough?

    def vars_for_template(self):
        seconds_to_mismatch = (self.player.wp_exit_time - datetime.now(timezone.utc)).total_seconds()
        return dict(seconds_to_mismatch=seconds_to_mismatch,
                    sec_to_min=int(Constants.sec_to_wait_on_wp/60))

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
