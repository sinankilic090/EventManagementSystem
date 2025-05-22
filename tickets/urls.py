from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('sepet/ekle/<int:etkinlik_id>/', views.sepet_ekle_view, name='sepet_ekle'),
    # Diğer ticket ile ilgili URL'ler varsa buraya ekleyebilirsin
]
