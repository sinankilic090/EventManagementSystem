# main/views.py

from django.shortcuts import render
from etkinlik.models import Etkinlik

def ana_sayfa(request):
    etkinlikler = Etkinlik.objects.filter(iptal_mi=False).order_by('tarih')  # İptal olmayan etkinlikler
    return render(request, 'main.html', {'etkinlikler': etkinlikler})
