from rest_framework import routers
from .viewsets import VignetteViewSet

vignette_router = routers.DefaultRouter()
vignette_router.register(r'vignettes', VignetteViewSet)
