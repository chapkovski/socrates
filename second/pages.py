from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Match
from datetime import datetime, timedelta, timezone
from first.generic_pages import GeneralVignettePage
from dateutil.relativedelta import relativedelta
from otree.live import live_payload_function


class FirstWP(WaitPage):
    pass

    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'


class DiscussionPage(GeneralVignettePage):
    live_method = 'chat'

    def is_displayed(self):
        return self.group.chat_status

    def before_next_page(self):
        self.group.chat_status = False
        for i in self.group.get_players():
            live_payload_function(i.participant.code, 'DiscussionPage', {'participant_left_chat': True})


class NoMatchingPage(Page):
    def is_displayed(self):
        return self.player.matched == Match.NOT_MATCHED


page_sequence = [
    FirstWP,
    DiscussionPage,
    NoMatchingPage,
]
