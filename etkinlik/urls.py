from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EtkinlikViewSet

router = DefaultRouter()
router.register(r'etkinlikler', EtkinlikViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
