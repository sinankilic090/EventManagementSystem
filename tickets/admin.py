from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'etkinlik', 'adet', 'toplam_fiyat', 'satin_alma_tarihi', 'satin_alindi')
    list_filter = ('satin_alma_tarihi', 'satin_alindi')  # satın alındı durumuna göre filtre ekledim
    search_fields = ('user__email', 'etkinlik__isim')
    readonly_fields = ('toplam_fiyat', 'satin_alma_tarihi')  # otomatik set edilen alanları readonly yapabilirsin
