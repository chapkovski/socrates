from django.urls import path, include
from second.models import Vignette, Param
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class VignetteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vignette
        fields = ['id', 'body', 'question', 'yes_option', 'no_option', 'title', 'correct']


class ParamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Param

        fields = ['id', 'name', 'body']
