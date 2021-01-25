from otree.api import Currency as c, currency_range
# from tester.generic_pages import oTreePage as Page
from ._builtin import WaitPage, Page
from pytz import timezone
from datetime import datetime
from django.utils.timezone import is_aware
from .models import Constants


class Timer(Page):


    def post(self):
        tts = self.subsession.time_to_start
        if datetime.now(tz=timezone('UTC')) < tts:
            return self._redirect_to_page_the_user_should_be_on()
        return super().post()

    def vars_for_template(self):
        tts = self.subsession.time_to_start

        seconds_till_start = (tts - datetime.now(tz=timezone('UTC'))).total_seconds()

        return dict(
            time_to_start_est=str(tts.astimezone(timezone('US/Eastern'))),
            time_to_start_cst=str(tts.astimezone(timezone('US/Central'))),
            time_to_start_pst=str(tts.astimezone(timezone('US/Pacific'))),
            time_bonus='time_bonus',
            seconds_till_start=seconds_till_start,
            on_time=seconds_till_start > -self.subsession.time_to_proceed

        )

    def before_next_page(self):
        self.player.set_times()




page_sequence = [
    Timer,

]
