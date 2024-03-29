from otree.api import (
    BaseSubsession,
    BasePlayer,
    models
)
from django.db import models as djmodels
from itertools import cycle


class VignetteSubsession(BaseSubsession):
    class Meta:
        abstract = True

    body = models.LongStringField()
    question = models.LongStringField()
    yes_option = models.LongStringField()
    no_option = models.LongStringField()
    vignette = djmodels.ForeignKey(to='Vignette', on_delete=djmodels.SET_NULL, blank=True, null=True)
    correct = models.BooleanField()

    def creating_session(self):
        from second.models import Vignette
        vignette_title = self.session.config.get('vignette')
        if not vignette_title:
            raise Exception('Vignette title is necessary')
        try:
            v = Vignette.objects.get(title=vignette_title)

        except Vignette.DoesNotExist:
            # THis is for debugging only!
            if vignette_title == 'asdf':
                v = Vignette.objects.create(title=vignette_title, body='Vignette example',
                                            question="what do you think?",
                                            yes_option='YES', no_option='NOPE', correct=True)
            else:
                raise Exception(f'Cannot find the vignette with the title "{vignette_title}"\n'
                                f'Go to "Vignette manager" and create the vignette with this title first!')
        self.vignette = v
        self.body = v.body
        self.question = v.question
        self.yes_option = v.yes_option
        self.no_option = v.no_option
        self.correct = v.correct


class VignettePlayer(BasePlayer):
    class Meta:
        abstract = True

    order = models.BooleanField()
    answer = models.BooleanField()
    confidence = models.IntegerField()

    def vignette_json(self):
        s = self.subsession
        choices = [dict(value=True, text=s.yes_option), dict(value=False, text=s.no_option)]
        if self.order:
            choices.reverse()

        return dict(
            body=s.body,
            q=s.question,
            choices=choices
        )

    def decision_making(self, payload, **kwargs):
        print(f'MESSAGE RECEIVED {payload} FROM: {self.id_in_group}')
