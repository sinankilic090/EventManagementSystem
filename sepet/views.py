from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from sepet.models import CartItem
from django.views.decorators.http import require_POST

def sepet_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("sign_in")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("sign_in")

    sepet_urunleri = CartItem.objects.filter(user=user)

    toplam_tutar = 0

    for item in sepet_urunleri:
        # CartItem modelindeki toplam_fiyat() metodunu kullanarak hesaplama
        item.birim_fiyat = 0
        if item.bilet_turu == 'vip':
            item.birim_fiyat = item.etkinlik.vip_fiyat
        elif item.bilet_turu == 'ogrenci':
            item.birim_fiyat = item.etkinlik.ogrenci_fiyat
        else:
            item.birim_fiyat = item.etkinlik.fiyat

        item.toplam_fiyat = item.toplam_fiyat()  # model metodunu çağırıyoruz

        toplam_tutar += item.toplam_fiyat

    context = {
        "sepet_urunleri": sepet_urunleri,
        "toplam_tutar": toplam_tutar,
    }
    return render(request, "sepet.html", context)

@require_POST
def sepetten_kaldir(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('sepet:sepet')
