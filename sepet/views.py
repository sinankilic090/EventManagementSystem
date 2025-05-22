from django.shortcuts import render, redirect
from users.models import User
from sepet.models import CartItem

def sepet_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("sign_in")

    sepet_urunleri = CartItem.objects.filter(user=user)
    toplam_tutar = sum(item.adet * item.etkinlik.fiyat for item in sepet_urunleri)

    context = {
        "sepet_urunleri": sepet_urunleri,
        "toplam_tutar": toplam_tutar,
    }
    return render(request, "sepet.html", context)
