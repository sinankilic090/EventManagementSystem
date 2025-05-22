from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),   
    path('users/', include('users.urls')),
    path('main/', include('main.urls')),
    path('tickets/', include('tickets.urls')),
    path('sepet/', include('sepet.urls')),
    path('payments/', include('payments.urls')), 
]
