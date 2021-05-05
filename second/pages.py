from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Match
from datetime import datetime, timedelta, timezone
from first.generic_pages import GeneralVignettePage
from second.generic_pages import Page
from otree.live import live_payload_function, _live_send_back
from first.pages import Opinion
from django.utils.html import escape

from .forms import CQForm


class FirstWP(WaitPage):
    template_name = 'second/MatcherWP.html'

    def is_displayed(self):
        now = datetime.now(timezone.utc)
        if not self.player.wp_entrance_time:
            self.player.wp_entrance_time = now
        if not self.player.wp_exit_time:
            self.player.wp_exit_time = now + timedelta(seconds=self.player.sec_waiting_too_long)

        return self.player.matched == Match.NOT_YET

    def vars_for_template(self):
        seconds_to_mismatch = (self.player.wp_exit_time - datetime.now(timezone.utc)).total_seconds()
        prog_val = (seconds_to_mismatch / self.player.sec_waiting_too_long) * 100
        return dict(seconds_to_mismatch=seconds_to_mismatch,
                    total_seconds_to_wait=self.player.sec_waiting_too_long,
                    val_now=int(prog_val),
                    val_for_progress=f"{prog_val / 100:.2%}",
                    sec_to_min=int(self.player.sec_waiting_too_long / 60))

    group_by_arrival_time = True
    after_all_players_arrive = 'when_matched'


class Instructions(Page):
    pass


class ComprehensionCheck(Page):
    time_tracker_field = 'time_on_comprehension_check'

    def get_form_class(self):
        return CQForm

class DiscussionAnnouncement(Page):
    # todo move this condition to some parents
    def is_displayed(self):
        return self.group.chat_status and self.player.matched == Match.MATCHED and self.player.in_chat_treatment


class BeforeDiscussionWP(WaitPage):
    after_all_players_arrive = 'set_timer'


class DiscussionPage(GeneralVignettePage):
    live_method = 'chat'
    time_tracker_field = 'time_on_discussion'
    _is_frozen = False

    def is_displayed(self):
        return self.group.chat_status and self.player.matched == Match.MATCHED and self.player.in_chat_treatment

    def before_next_page(self):
        self.group.chat_status = False

    def post(self):
        # TODO: check if they are allowed to leave
        if not self.participant._is_bot:
            for i in self.player.get_others_in_group():
                pcode_retval = {i.participant.code: {'participant_left_chat': True, 'action': 'endOfChat'}}
                _live_send_back(i.participant._session_code, i.participant._index_in_pages,
                                pcode_retval
                                )

        return super().post()


class NoMatchingPage(Page):
    def is_displayed(self):
        # If this is the essay type of treatment we don't get to No matching page anyway
        if not self.player.in_chat_treatment:
            return False
        return self.player.matched == Match.NOT_MATCHED


class EssayPage(GeneralVignettePage):
    time_tracker_field = 'time_on_essay'
    form_model = 'player'
    form_fields = ['essay']

    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)
        form = c.get('form')

        if form and hasattr(form, 'cleaned_data'):
            form_data = form.cleaned_data
            for k, v in form_data.items():
                form_data[k] = escape(v)
            c['form_data'] = form_data
        return c

    def post(self):
        if not self.participant._is_bot:
            if self.group.seconds_till_allow_to_leave > 0:
                self.object = self.get_object()
                form = self.get_form(data=self.request.POST, files=self.request.FILES, instance=self.object)
                return self.form_invalid(form)
        return super().post()

    def is_displayed(self):
        return not self.player.in_chat_treatment


class BeforeSecondOpinion(Page):
    pass


class SecondOpinion(Opinion):
    time_tracker_field = 'time_on_second_opinion'
    template_name = 'first/Opinion.html'
    form_model = 'player'
    form_fields = ['answer', 'confidence']


class AfterDiscussionWP(WaitPage):
    after_all_players_arrive = 'set_payoffs_and_results'


class Results(Page):
    pass


page_sequence = [
    FirstWP,
    Instructions,
    ComprehensionCheck,
    DiscussionAnnouncement,
    BeforeDiscussionWP,
    DiscussionPage,
    EssayPage,
    NoMatchingPage,
    BeforeSecondOpinion,
    SecondOpinion,
    AfterDiscussionWP
]
