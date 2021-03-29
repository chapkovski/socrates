from second.models import Vignette, Param
from rest_framework import viewsets
from .serializers import VignetteSerializer, ParamSerializer


class VignetteViewSet(viewsets.ModelViewSet):
    queryset = Vignette.objects.all()
    serializer_class = VignetteSerializer


class ParamViewSet(viewsets.ModelViewSet):
    queryset = Param.objects.all()
    serializer_class = ParamSerializer
