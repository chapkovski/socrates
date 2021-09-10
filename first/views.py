from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from otree.models import Participant
from django.views.generic import ListView
from otree.models import Session
from django.shortcuts import redirect, reverse
import pandas as pd


class GetCurrentVignette(View):
    url_pattern = 'vignette/<str:participant_code>'
    url_name = 'get_current_vignette'

    def get(self, request, *args, **kwargs):
        try:
            participant = Participant.objects.get(code=self.kwargs.get('participant_code'))
        except Participant.DoesNotExist:
            resp = dict(error=True)
            return JsonResponse(resp)
        p = participant.first_player.first() or participant.second_player.first() or participant.prol_player.first()
        if p:
            resp = p.vignette_json()

        else:
            resp = dict(error=True)
        return JsonResponse(resp)


class CustomSessionList(ListView):
    model = Session
    url_pattern = 'customexport/sessions'
    url_name = 'custom_sessions'
    display_name = 'Custom export (including payoffs csv)'
    template_name = 'customexport/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return self.model.objects.filter(participant__label__isnull=False).distinct()


class PandasExport(View):
    url_name = 'export_payoffs'
    url_pattern = fr'custom_export/<session_code>/payoff'
    content_type = 'text/csv'

    def get(self, request, *args, **kwargs):

        session = Session.objects.get(code=kwargs.get('session_code'))
        parts = Participant.objects.filter(session=session, label__isnull=False, payoff__isnull=False).values('label',
                                                                                                              'payoff')
        participation_fee = session.config['participation_fee']
        df = pd.DataFrame(data=parts)
        if df is not None and not df.empty:
            df.payoff = df.payoff
            df.payoff = df.payoff.astype('float')
            csv_data = df.to_csv(header=False, index=False)
            response = HttpResponse(csv_data, content_type=self.content_type)
            filename = f'{session.code}_payoffs.csv'
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        else:
            return redirect(reverse('custom_sessions'))
