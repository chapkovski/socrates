from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse
from second.models import Vignette
from otree.models import Participant
from rest_framework.authtoken.models import Token
from django.utils.safestring import mark_safe


class GetCurrentVignette(View):
    url_pattern = 'vignette/<str:participant_code>'
    url_name = 'get_current_vignette'

    def get(self, request, *args, **kwargs):
        try:
            participant = Participant.objects.get(code=self.kwargs.get('participant_code'))
        except Participant.DoesNotExist:
            resp = dict(error=True)
            return JsonResponse(resp)
        p = participant.first_player.first() or participant.second_player.first()
        if p:
            resp = p.vignette_json()

        else:
            resp = dict(error=True)
        return JsonResponse(resp)
