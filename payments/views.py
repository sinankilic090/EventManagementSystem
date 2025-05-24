from django.shortcuts import render, redirect
from sepet.models import CartItem
from tickets.models import Ticket
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Payment

@login_required
def kart_ile_odeme(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('sepet:sepet')  # sepet boşsa

    toplam_tutar = sum(item.toplam_fiyat() for item in cart_items)

    if request.method == "POST":
        card_holder = request.POST.get("card_holder")
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        installments = int(request.POST.get("installments", 1))

        if not all([card_holder, card_number, expiry_date, cvv]):
            return render(request, "kart_odeme.html", {
                'amount': toplam_tutar,
                'error': "Lütfen tüm alanları doldurun."
            })

        try:
            with transaction.atomic():
                for item in cart_items:
                    etkinlik = item.etkinlik
                    if etkinlik.kalan_bilet < item.adet:
                        raise ValueError(f"'{etkinlik.isim}' etkinliğinde yeterli bilet yok!")

                Payment.objects.create(
                    user=user,
                    card_holder=card_holder,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    amount=toplam_tutar,
                    payment_type='kart',
                    installments=installments
                )

                for item in cart_items:
                    etkinlik = item.etkinlik
                    #etkinlik.kalan_bilet -= item.adet
                    etkinlik.save()

                    Ticket.objects.create(
                        user=user,
                        etkinlik=etkinlik,
                        adet=item.adet
                    )

                cart_items.delete()

        except ValueError as e:
            return render(request, "kart_odeme.html", {
                'amount': toplam_tutar,
                'error': str(e)
            })

        return render(request, "success.html")

    return render(request, "kart_odeme.html", {
        'amount': toplam_tutar
    })


@login_required
def eft_ile_odeme(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('sepet:sepet')

    toplam_tutar = sum(item.toplam_fiyat() for item in cart_items)

    if request.method == "POST":
        try:
            with transaction.atomic():
                for item in cart_items:
                    etkinlik = item.etkinlik
                    if etkinlik.kalan_bilet < item.adet:
                        raise ValueError(f"'{etkinlik.isim}' etkinliğinde yeterli bilet yok!")

                Payment.objects.create(
                    user=user,
                    payment_type='eft',
                    amount=toplam_tutar
                )

                for item in cart_items:
                    etkinlik = item.etkinlik
                    #etkinlik.kalan_bilet -= item.adet
                    etkinlik.save()

                    Ticket.objects.create(
                        user=user,
                        etkinlik=etkinlik,
                        adet=item.adet
                    )

                cart_items.delete()

        except ValueError as e:
            return render(request, "eft_odeme.html", {
                'amount': toplam_tutar,
                'error': str(e)
            })

        return render(request, "success.html")

    return render(request, "eft_odeme.html", {
        'amount': toplam_tutar
    })
