from django.contrib import admin
from .models import Etkinlik
from .hava_api import hava_durumu_kotu_mu  # Hava durumu fonksiyonunu import et

@admin.register(Etkinlik)
class EtkinlikAdmin(admin.ModelAdmin):
    list_display = ('isim', 'tarih', 'sehir', 'konum', 'toplam_bilet', 'kalan_bilet', 'iptal_mi', 'tur', 'fiyat')
    search_fields = ('isim', 'sehir', 'tur')
    list_filter = ('iptal_mi', 'tarih', 'tur')

    def save_model(self, request, obj, form, change):
        # Türlere göre varsayılan fiyatlar
        default_fiyatlar = {
            'konser': 200.00,
            'tiyatro': 400.00,
            'film': 100.00,
            'sergi': 150.00,
            'diger': 120.00,
        }

        # Fiyat boşsa veya 0 ise türüne göre fiyat ata
        if not obj.fiyat or obj.fiyat == 0:
            obj.fiyat = default_fiyatlar.get(obj.tur.lower(), 100.00)  # tür yoksa 100 TL default

        # Hava durumu kontrolü, iptal_mi alanını güncelle
        obj.iptal_mi = hava_durumu_kotu_mu(obj.sehir)

        super().save_model(request, obj, form, change)
