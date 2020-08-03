from t.models import Vignette
from rest_framework import  viewsets
from .serializers import   VignetteSerializer

class VignetteViewSet(viewsets.ModelViewSet):
    queryset = Vignette.objects.all()
    serializer_class = VignetteSerializer