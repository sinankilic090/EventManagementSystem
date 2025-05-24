from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('kart/', views.kart_ile_odeme, name='kart_ile_odeme'),  # Kartla ödeme sayfası
    path('eft/', views.eft_ile_odeme, name='eft_ile_odeme'),     # EFT/Havale ödeme sayfası
]
