from django.shortcuts import render, redirect
from sepet.models import CartItem
from tickets.models import Ticket
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Payment

@login_required
def payment_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('sepet_list')

    toplam_tutar = sum(item.toplam_fiyat() for item in cart_items)

    if request.method == "POST":
        card_holder = request.POST.get("card_holder")
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        payment_type = request.POST.get("payment_type")
        installments = int(request.POST.get("installments", 1))

        if not all([card_holder, card_number, expiry_date, cvv]):
            return render(request, "payment_form.html", {
                'amount': toplam_tutar,
                'error': "Lütfen tüm alanları doldurun."
            })

        # Transaction başlat
        try:
            with transaction.atomic():
                # Öncelikle etkinlik bilet stok kontrolü
                for item in cart_items:
                    etkinlik = item.etkinlik
                    if etkinlik.kalan_bilet < item.adet:
                        raise ValueError(f"'{etkinlik.isim}' etkinliğinde yeterli bilet yok!")

                # Ödeme kaydı oluştur
                Payment.objects.create(
                    user=user,
                    card_holder=card_holder,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    amount=toplam_tutar,
                    payment_type=payment_type,
                    installments=installments
                )

                # Bilet stok güncelle ve ticket oluştur
                for item in cart_items:
                    etkinlik = item.etkinlik
                    etkinlik.kalan_bilet -= item.adet
                    etkinlik.save()

                    Ticket.objects.create(
                        user=user,
                        etkinlik=etkinlik,
                        adet=item.adet
                    )

                # Sepeti boşalt
                cart_items.delete()

        except ValueError as e:
            return render(request, "payment_form.html", {
                'amount': toplam_tutar,
                'error': str(e)
            })

        return render(request, "success.html")

    return render(request, "payment_form.html", {
        'amount': toplam_tutar
    })
