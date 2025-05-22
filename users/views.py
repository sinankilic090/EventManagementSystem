from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from .models import User
from django.http import HttpResponse

def test_session_view(request):
    user_id = request.session.get("user_id")
    if user_id:
        return HttpResponse(f"Giriş yapılmış. Kullanıcı ID: {user_id}")
    else:
        return HttpResponse("Giriş yapılmamış.")



def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email ve şifre boş bırakılamaz.")
            return redirect('users:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email zaten kayıtlı.")
            return redirect('users:register')

        user = User.objects.create(
            email=email,
            password=make_password(password),
            is_admin=False,
            is_approved=False,
        )

        messages.success(request, "Kayıt başarılı! Admin onayı bekleniyor.")
        return redirect('users:sign_in')

    return render(request, 'register.html')


def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email ve şifre boş bırakılamaz.")
            return redirect('users:sign_in')

        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(request, "Email bulunamadı.")
            return redirect('users:sign_in')

        if not user.is_approved:
            messages.error(request, "Admin onayı bekleniyor.")
            return redirect('users:sign_in')

        if not check_password(password, user.password):
            messages.error(request, "Şifre yanlış.")
            return redirect('users:sign_in')

        login(request, user)

        # ✅ Oturum ID'yi manuel olarak kaydet
        request.session["user_id"] = user.id

        if user.must_change_password:
            return redirect('users:change_password')

        return redirect('main')

    return render(request, 'sign_in.html')



@login_required(login_url='users:sign_in')
def change_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        if not new_password:
            messages.error(request, "Yeni şifre boş olamaz.")
            return redirect('users:change_password')

        request.user.password = make_password(new_password)
        request.user.must_change_password = False
        request.user.save()

        messages.success(request, "Şifreniz başarıyla değiştirildi.")
        return redirect('users:sign_in')

    return render(request, 'change_password.html')
