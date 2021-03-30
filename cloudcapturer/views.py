from django.views.generic import ListView, View, DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.utils.translation import ugettext as _
import logging
from otree.models import Session
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from otree.views.participant import participant_or_none_if_exceeded, no_participants_left_http_response

logger = logging.getLogger(__name__)


class CloudRedirector(RedirectView):
    url_name = 'cloud_redirector'
    url_pattern = 'cloud/<str:session_code>/'
    pattern_name = 'home'

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if not url:
            return HttpResponseNotFound(_("Session is full."))
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        session = get_object_or_404(Session, code=kwargs['session_code'])
        all_participants = session.participant_set.all()
        hitId = self.request.GET.get('hitId')
        workerId = self.request.GET.get('workerId')
        if hitId and workerId:
            candidates = [i for i in all_participants if i.vars.get('hitId') == hitId and
                          i.vars.get('workerId') == workerId]
        else:
            candidates = None
        if candidates:
            participant = candidates[0]
        else:
            participant = session.participant_set.filter(visited=False).order_by('id').first()
        if participant:
            participant.vars.update(**self.request.GET.dict())
            participant.label = workerId
            participant.save()
            return participant._url_i_should_be_on()


