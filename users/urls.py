from django.urls import path
from . import views
from .views import test_session_view

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('sign-in/', views.sign_in_view, name='sign_in'), 
    path('change-password/', views.change_password_view, name='change_password'),
    path('test-session/', test_session_view, name='test_session'),

]