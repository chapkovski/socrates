from django.urls import path, include, re_path
from rest_framework.authtoken import views
from second.views import TestView, AxiosView, InstructionManager
from second.drf import vignette_router


def path_wrapper(view):
    return path(view.url_pattern, view.as_view(), name=view.url_name)


urlpatterns = [
    path('api-token-auth', views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),
    path('api/', include(vignette_router.urls)),
    re_path(TestView.url_pattern, TestView.as_view(), name=TestView.url_name),
    re_path(AxiosView.url_pattern, AxiosView.as_view(), name=AxiosView.url_name),
    re_path(InstructionManager.url_pattern, InstructionManager.as_view(), name=InstructionManager.url_name),
]
