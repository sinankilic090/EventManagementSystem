from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Etkinlik
from .serializers import EtkinlikSerializer

class EtkinlikViewSet(viewsets.ModelViewSet):
    queryset = Etkinlik.objects.all()
    serializer_class = EtkinlikSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
