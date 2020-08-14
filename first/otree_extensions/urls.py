from django.urls import path, include, re_path
from first.views import GetCurrentVignette

urlpatterns = [
    path(GetCurrentVignette.url_pattern, GetCurrentVignette.as_view(), name=GetCurrentVignette.url_name),
]
