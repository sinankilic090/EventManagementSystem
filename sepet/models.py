# sepet/models.py
from django.db import models
from etkinlik.models import Etkinlik
from users.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField(default=1)

    def toplam_fiyat(self):
        return self.adet * self.etkinlik.fiyat

    def __str__(self):
        return f"{self.user.email} - {self.etkinlik.isim} - {self.adet} adet"
