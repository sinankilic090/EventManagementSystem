from django.core.management.base import BaseCommand
from etkinlik.models import Etkinlik
from etkinlik.hava_api import hava_durumu_kotu_mu  # Bu fonksiyon senin verdiğin fonksiyon

class Command(BaseCommand):
    help = 'Etkinliklerin hava durumuna göre iptal durumlarını günceller'

    def handle(self, *args, **kwargs):
        etkinlikler = Etkinlik.objects.all()
        for etkinlik in etkinlikler:
            kötü_hava = hava_durumu_kotu_mu(etkinlik.sehir)
            if kötü_hava:
                etkinlik.iptal_mi = True
            else:
                etkinlik.iptal_mi = False
            etkinlik.save()
            self.stdout.write(f"{etkinlik.isim} - {etkinlik.sehir} - İptal: {etkinlik.iptal_mi}")
