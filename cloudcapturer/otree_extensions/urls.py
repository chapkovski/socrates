from django.urls import path
from cloudcapturer.views import CloudRedirector

views_to_add = [
    CloudRedirector
]
urlpatterns = [path(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]
