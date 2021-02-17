from first.generic_pages import GeneralVignettePage
from second.models import TimeTracker

class Opinion(GeneralVignettePage):

    time_tracker_field = 'time_on_first_opinion'
    live_method = 'decision_making'
    form_model = 'player'
    form_fields = ['answer', 'confidence', 'timezone']

    def is_displayed(self):
        return True

    def before_next_page(self):
        self.participant.vars['position'] = int(self.player.answer)


page_sequence = [Opinion]
