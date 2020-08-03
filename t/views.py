from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse

from rest_framework.authtoken.models import Token


class TestView(TemplateView):
    url_pattern = r'vignettemanager/.*$'
    url_name = 'TTT'
    template_name = 't/admin/create_vignette.html'

    def get(self, request, *args, **kwargs):
        print('USER:', request.user)
        return super().get(request, *args, **kwargs)


class AxiosView(View):
    url_pattern = r'ax/.*$'
    url_name = 'ax'

    def get(self, request, *args, **kwargs):
        print('USER:', request.user)
        print('USER AUTH:', request.user.is_authenticated)
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)

            return JsonResponse(dict(token=token.key))
        return JsonResponse(dict(token='hui!'))
