from django.urls import path, include, re_path
from first.views import GetCurrentVignette, PandasExport

urlpatterns = [
    path(GetCurrentVignette.url_pattern, GetCurrentVignette.as_view(), name=GetCurrentVignette.url_name),
    path(PandasExport.url_pattern, PandasExport.as_view(), name=PandasExport.url_name),
]
