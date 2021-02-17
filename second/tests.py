from otree.api import Currency as c, currency_range, Submission
from .pages import *
from ._builtin import Bot
import random

class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        yield ComprehensionCheck, {'cq_3': True, 'cq_6': True, 'cq_4': True}
        if  self.group.chat_status and self.player.matched == Match.MATCHED and self.session.config.get('chat'):
            yield Submission(DiscussionPage)
        if not self.session.config.get('chat'):
            yield EssayPage, {'essay': 'bot essay'}
        if self.player.matched == Match.NOT_MATCHED and self.session.config.get('chat'):
            yield NoMatchingPage,

        ans = dict(
            confidence=random.randint(0, 10),
            answer=random.choice([True, False])
        )
        yield Submission(SecondOpinion, ans, check_html=False)

