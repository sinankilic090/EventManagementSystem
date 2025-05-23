from django.urls import path
from . import views

app_name = 'sepet'

urlpatterns = [
    path('', views.sepet_view, name='sepet'),
    # Ödeme sayfası gibi başka url'ler varsa buraya ekleyebilirsin
    # Örnek:
    # path('odeme/', views.odeme_view, name='odeme'),
    path('kaldir/<int:item_id>/', views.sepetten_kaldir, name='sepetten_kaldir'),

]
