from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse
from .models import Vignette
from rest_framework.authtoken.models import Token
from django.utils.safestring import mark_safe


class GetCurrentVignette(View):
    url_pattern = 'vignette/<str:participant_code>'
    url_name = 'get_current_vignette'

    def get(self, request, *args, **kwargs):
        """Here we'll return a vignette based on participant code and player id"""
        """Lets firrst return a first vignette"""
        v = Vignette.objects.all().first()
        return JsonResponse(dict(body=mark_safe(v.body)))


class TestView(TemplateView):
    url_pattern = r'vignettemanager/.*$'
    url_name = 'vignette_manager'
    template_name = 'second/admin/create_vignette.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
class InstructionManager(TemplateView):
    url_pattern = r'instructions/.*$'
    url_name = 'instruction_manager'
    template_name = 'second/admin/instruction_manager.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AxiosView(View):
    url_pattern = r'ax/.*$'
    url_name = 'ax'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            return JsonResponse(dict(token=token.key))
        return JsonResponse(dict(token='hui!'))
