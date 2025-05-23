from django.shortcuts import render
from etkinlik.models import Etkinlik
from duyurular.models import Duyuru  # Duyuru modelini ekliyoruz

def ana_sayfa(request):
    etkinlikler = Etkinlik.objects.filter(iptal_mi=False).order_by('tarih')  # İptal olmayan etkinlikler
    duyurular = Duyuru.objects.all().order_by('-tarih')[:5]  # En yeni 5 duyuruyu al
    return render(request, 'main.html', {
        'etkinlikler': etkinlikler,
        'duyurular': duyurular
    })
