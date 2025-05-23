from django.db import models

class Etkinlik(models.Model):
    ETKINLIK_TURLERI = [
        ('konser', 'Konser'),
        ('tiyatro', 'Tiyatro'),
        ('film', 'Film'),
        ('sergi', 'Sergi'),
        ('diger', 'Diğer'),
    ]

    isim = models.CharField(max_length=255)
    tarih = models.DateTimeField()
    toplam_bilet = models.IntegerField()
    kalan_bilet = models.IntegerField()
    iptal_mi = models.BooleanField(default=False)
    sehir = models.CharField(max_length=100)
    konum = models.TextField()
    fiyat = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)      # Standart fiyat
    vip_fiyat = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # VIP fiyat
    ogrenci_fiyat = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) # Öğrenci fiyatı
    tur = models.CharField(max_length=20, choices=ETKINLIK_TURLERI, default='diger')
    image_url = models.URLField(
        default="https://via.placeholder.com/300x200.png?text=Etkinlik+Görseli",
        verbose_name="Etkinlik Görseli"
    )

    def __str__(self):
        return self.isim
