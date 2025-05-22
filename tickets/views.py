from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from etkinlik.models import Etkinlik
from sepet.models import CartItem
from .models import Ticket
from users.models import User
from django.utils.timezone import now

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
        try:
            adet = int(request.POST.get("adet", 1))
        except ValueError:
            adet = 1

        if adet < 1:
            adet = 1

        if event.kalan_bilet == 0:
            error_message = "Biletler tükenmiştir."
            messages.error(request, error_message)
        elif adet > event.kalan_bilet:
            error_message = "Stoktan fazla bilet ekleyemezsiniz."
            messages.error(request, error_message)
        else:
            existing_item = CartItem.objects.filter(user=user, etkinlik=event).first()
            if existing_item:
                existing_item.adet += adet
                existing_item.save()
            else:
                CartItem.objects.create(user=user, etkinlik=event, adet=adet)

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

    total_price = sum(item.adet * item.etkinlik.fiyat for item in cart_items)

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
        Ticket.objects.create(
            user=user,
            etkinlik=etkinlik,
            adet=item.adet,
            satin_alma_tarihi=now(),
            toplam_fiyat=item.adet * etkinlik.fiyat
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
