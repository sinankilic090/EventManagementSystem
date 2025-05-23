from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from etkinlik.models import Etkinlik
from sepet.models import CartItem
from .models import Ticket
from users.models import User
from django.utils.timezone import now

# Helper: bilet türüne göre fiyatı al
def get_bilet_fiyati(event, bilet_turu):
    if bilet_turu == "vip":
        return event.vip_fiyat or 0
    elif bilet_turu == "ogrenci":
        return event.ogrenci_fiyat or 0
    else:
        return event.fiyat or 0

# Sepete Ekle
def sepet_ekle_view(request, etkinlik_id):
    event = get_object_or_404(Etkinlik, id=etkinlik_id)
    error_message = None

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("sign_in")

    if request.method == "POST":
        adet = int(request.POST.get("adet", 1))
        bilet_turu = request.POST.get("bilet_turu", "normal")

        if adet < 1:
            adet = 1

        if event.kalan_bilet == 0:
            error_message = "Biletler tükenmiştir."
            messages.error(request, error_message)
        elif adet > event.kalan_bilet:
            error_message = "Stoktan fazla bilet ekleyemezsiniz."
            messages.error(request, error_message)
        else:
            existing_item = CartItem.objects.filter(user=user, etkinlik=event, bilet_turu=bilet_turu).first()
            if existing_item:
                existing_item.adet += adet
                existing_item.save()
            else:
                CartItem.objects.create(user=user, etkinlik=event, adet=adet, bilet_turu=bilet_turu)

            messages.success(request, "Etkinlik sepete eklendi.")
            return redirect("main")

    return render(request, "ticket.html", {
        'event': event,
        'remaining_tickets': event.kalan_bilet,
        'error_message': error_message,
    })


# Sepeti Görüntüle
def sepet_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    user = get_object_or_404(User, pk=user_id)
    cart_items = CartItem.objects.filter(user=user)

    total_price = 0
    for item in cart_items:
        fiyat = get_bilet_fiyati(item.etkinlik, item.bilet_turu)
        total_price += item.adet * fiyat

    return render(request, "sepet.html", {
        'cart_items': cart_items,
        'total_price': total_price,
    })


# Satın Alma İşlemi
def satin_al_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    user = get_object_or_404(User, pk=user_id)
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Sepetiniz boş.")
        return redirect("sepet")

    for item in cart_items:
        etkinlik = item.etkinlik
        if etkinlik.kalan_bilet < item.adet:
            messages.error(request, f"{etkinlik.isim} için yeterli bilet yok.")
            return redirect("sepet")

    # Hepsi uygunsa satın al
    for item in cart_items:
        etkinlik = item.etkinlik
        fiyat = get_bilet_fiyati(etkinlik, item.bilet_turu)

        Ticket.objects.create(
            user=user,
            etkinlik=etkinlik,
            adet=item.adet,
            satin_alma_tarihi=now(),
            toplam_fiyat=item.adet * fiyat,
            bilet_turu=item.bilet_turu
        )
        etkinlik.kalan_bilet -= item.adet
        etkinlik.save()

    cart_items.delete()
    messages.success(request, "Biletler başarıyla satın alındı!")
    return redirect("biletlerim")


# Kullanıcının satın aldığı biletleri göster
def biletlerim_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    user = get_object_or_404(User, pk=user_id)
    tickets = Ticket.objects.filter(user=user)

    return render(request, "biletlerim.html", {
        'tickets': tickets,
    })
