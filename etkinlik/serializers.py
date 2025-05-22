from rest_framework import serializers
from .models import Etkinlik

class EtkinlikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etkinlik
        fields = '__all__'
