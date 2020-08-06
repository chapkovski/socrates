from django.urls import path, include, re_path
from rest_framework.authtoken import views
from t.views import TestView, AxiosView, GetCurrentVignette
from t.drf import vignette_router

print('ROUTER PATHS', vignette_router.urls)


def path_wrapper(view):
    return path(view.url_pattern, view.as_view(), name=view.url_name)


urlpatterns = [
    path('api-token-auth', views.obtain_auth_token),
    path('api-auth', include('rest_framework.urls')),
    path('api/', include(vignette_router.urls)),
    re_path(TestView.url_pattern, TestView.as_view(), name=TestView.url_name),
    re_path(AxiosView.url_pattern, AxiosView.as_view(), name=AxiosView.url_name),
    path_wrapper(GetCurrentVignette)
]
