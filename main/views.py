from django.shortcuts import render
from etkinlik.models import Etkinlik
from duyurular.models import Duyuru

def ana_sayfa(request):
    TUR_LISTESI = ['konser', 'tiyatro', 'film', 'sergi', 'diger']
    secilen_turler = request.GET.getlist('tur')

    etkinlikler = Etkinlik.objects.filter(iptal_mi=False).order_by('-tarih')
    duyurular = Duyuru.objects.all().order_by('-tarih')[:5]

    if secilen_turler:
        filtreli_etkinlikler = etkinlikler.filter(tur__in=secilen_turler)
    else:
        filtreli_etkinlikler = []

    print("Seçilen türler:", secilen_turler)  # debug
    print("Filtreli etkinlikler sayısı:", filtreli_etkinlikler.count() if filtreli_etkinlikler else 0)

    return render(request, 'main.html', {
        'etkinlikler': etkinlikler,
        'duyurular': duyurular,
        'turler': TUR_LISTESI,
        'secilen_turler': secilen_turler,
        'filtreli_etkinlikler': filtreli_etkinlikler,
    })
