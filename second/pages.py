from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Match
from datetime import datetime, timedelta, timezone
from first.generic_pages import GeneralVignettePage
from dateutil.relativedelta import relativedelta

class FirstWP(WaitPage):
    template_name = 'second/MatcherWP.html'

    def is_displayed(self):
        now = datetime.now(timezone.utc)
        if not self.player.wp_entrance_time:
            self.player.wp_entrance_time = now
        if not self.player.wp_exit_time:
            self.player.wp_exit_time = now + timedelta(seconds=self.session.config.get('sec_to_wait_on_wp'))

        return self.player.matched == Match.NOT_YET

    def vars_for_template(self):
        seconds_to_mismatch = (self.player.wp_exit_time - datetime.now(timezone.utc)).total_seconds()
        return dict(seconds_to_mismatch=seconds_to_mismatch,
                    sec_to_min=int(self.session.config.get('sec_to_wait_on_wp') / 60))

    group_by_arrival_time = True
    after_all_players_arrive = 'set_timer'


class DiscussionPage(GeneralVignettePage):
    live_method = 'chat'

    def vars_for_template(self):
        time_to_exit = (datetime.now() + relativedelta(seconds=60)).strftime("%Y/%m/%d, %H:%M:%S")
        print("PIZDA", time_to_exit)
        print("JOPA NOW", datetime.now())
        return dict(
            time_to_exit=time_to_exit
        )

    def is_displayed(self):
        return self.player.matched == Match.MATCHED


class NoMatchingPage(Page):
    def is_displayed(self):
        return self.player.matched == Match.NOT_MATCHED


page_sequence = [
    FirstWP,
    DiscussionPage,
    NoMatchingPage,
]
