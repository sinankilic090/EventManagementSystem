from django.db import models

class Duyuru(models.Model):
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik
