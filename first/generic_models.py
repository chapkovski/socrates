from otree.api import (
    BaseSubsession,
    BasePlayer,
    models
)
from django.db import models as djmodels


class VignetteSubsession(BaseSubsession):
    class Meta:
        abstract = True

    body = models.LongStringField()
    question = models.LongStringField()
    yes_option = models.LongStringField()
    no_option = models.LongStringField()
    vignette = djmodels.ForeignKey(to='Vignette', on_delete=djmodels.SET_NULL, blank=True, null=True)

    def creating_session(self):
        from t.models import Vignette
        vignette_title = self.session.config.get('vignette')
        if not vignette_title:
            raise Exception('Vignette title is necessary')
        try:
            v = Vignette.objects.get(title=vignette_title)
            self.vignette = v
            self.body = v.body
            self.question = v.question
            self.yes_option = v.yes_option
            self.no_option = v.no_option
        except Vignette.DoesNotExist:
            raise Exception('Cannot find the vignette')


class VignettePlayer(BasePlayer):
    class Meta:
        abstract = True

    order = models.BooleanField()
    answer = models.BooleanField()
    confidence = models.IntegerField()

    def vignette_json(self):
        s = self.subsession
        print('BODY', s.body)
        choices = [dict(value=True, text=s.yes_option), dict(value=False, text=s.no_option)]
        if self.order:
            choices.reverse()

        return dict(
            body=s.body,
            q=s.question,
            choices=choices
        )
