from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from users.models import User
from etkinlik.models import Etkinlik

class Ticket(models.Model):
    BILET_TURLERI = [
        ('standart', 'Standart'),
        ('vip', 'VIP'),
        ('ogrenci', 'Öğrenci'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField()
    bilet_turu = models.CharField(max_length=10, choices=BILET_TURLERI, default='standart')
    satin_alma_tarihi = models.DateTimeField(null=True, blank=True)
    toplam_fiyat = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    satin_alindi = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.etkinlik.kalan_bilet < self.adet:
                raise ValidationError("Yeterli bilet kalmamış.")
            self.etkinlik.kalan_bilet -= self.adet
            self.etkinlik.save()

        if self.satin_alindi and self.satin_alma_tarihi is None:
            self.satin_alma_tarihi = now()

        # Bilet türüne göre fiyat hesapla
        if self.bilet_turu == 'vip':
            fiyat = self.etkinlik.vip_fiyat
        elif self.bilet_turu == 'ogrenci':
            fiyat = self.etkinlik.ogrenci_fiyat
        else:
            fiyat = self.etkinlik.fiyat

        self.toplam_fiyat = self.adet * fiyat
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.etkinlik.isim} - {self.adet} adet - {self.bilet_turu} - Satın alındı: {self.satin_alindi}"
