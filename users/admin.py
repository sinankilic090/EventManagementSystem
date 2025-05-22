from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'is_admin', 'is_approved', 'must_change_password', 'is_active', 'is_staff', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_admin', 'is_approved', 'must_change_password')
    list_filter = ('is_admin', 'is_approved')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_approved', 'must_change_password', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
