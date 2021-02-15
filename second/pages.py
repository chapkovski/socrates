from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Match
from datetime import datetime, timedelta, timezone
from first.generic_pages import GeneralVignettePage
from dateutil.relativedelta import relativedelta
from otree.live import live_payload_function
from first.pages import Opinion
from django.utils.html import escape


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


class Instructions(Page):
    pass


from .forms import CQForm


class ComprehensionCheck(Page):
    def get_form_class(self):
        return CQForm


class BeforeDiscussionWP(WaitPage):
    pass


class DiscussionPage(GeneralVignettePage):
    live_method = 'chat'
    _is_frozen = False

    def is_displayed(self):
        return self.group.chat_status and self.player.matched and self.session.config.get('chat')

    def before_next_page(self):
        self.group.chat_status = False

    def post(self):
        # TODO: check if they are allowed to leave
        for i in self.group.get_players():
            live_payload_function(i.participant.code, 'DiscussionPage',
                                  {'participant_left_chat': True, 'action': 'endOfChat'})

        return super().post()


class NoMatchingPage(Page):
    def is_displayed(self):
        # If this is the essay type of treatment we don't get to No matching page anyway
        if not self.session.config.get('chat'):
            return False
        return self.player.matched == Match.NOT_MATCHED


class EssayPage(GeneralVignettePage):
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
        if self.group.seconds_till_allow_to_leave > 0:
            self.object = self.get_object()
            form = self.get_form(data=self.request.POST, files=self.request.FILES, instance=self.object)
            return self.form_invalid(form)
        return super().post()

    def is_displayed(self):
        return not self.session.config.get('chat')


class SecondOpinion(Opinion):
    template_name = 'first/Opinion.html'
    form_model = 'player'
    form_fields = ['answer', 'confidence']


class AfterDiscussionWP(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [
    FirstWP,
    Instructions,
    ComprehensionCheck,
    BeforeDiscussionWP,
    DiscussionPage,
    EssayPage,
    NoMatchingPage,
    SecondOpinion,
    AfterDiscussionWP
]
