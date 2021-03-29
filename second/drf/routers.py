from rest_framework import routers
from .viewsets import VignetteViewSet, ParamViewSet

vignette_router = routers.DefaultRouter()
vignette_router.register(r'vignettes', VignetteViewSet)
vignette_router.register(r'params', ParamViewSet)
