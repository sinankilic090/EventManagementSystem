from django.db import models
from etkinlik.models import Etkinlik
from users.models import User

class CartItem(models.Model):
    BILET_TURLERI = [
        ('standart', 'Standart'),
        ('vip', 'VIP'),
        ('ogrenci', 'Öğrenci'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField(default=1)
    bilet_turu = models.CharField(max_length=10, choices=BILET_TURLERI, default='standart')

    def toplam_fiyat(self):
        if self.bilet_turu == 'vip':
            fiyat = self.etkinlik.vip_fiyat
        elif self.bilet_turu == 'ogrenci':
            fiyat = self.etkinlik.ogrenci_fiyat
        else:
            fiyat = self.etkinlik.fiyat
        return self.adet * fiyat

    def __str__(self):
        return f"{self.user.email} - {self.etkinlik.isim} - {self.adet} adet - {self.bilet_turu}"
