from django.db import models
from django.conf import settings

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('single', 'Single Payment'),
        ('installment', 'Installment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    card_holder = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # MM/YY
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    installments = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.payment_type} - {self.amount}₺"

    def clean(self):
        # Burada model temizliği için doğrulama yapabiliriz
        from django.core.exceptions import ValidationError
        if self.payment_type == 'single' and self.installments != 1:
            raise ValidationError("Single payment should have installments=1.")
