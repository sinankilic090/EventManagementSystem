from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('single', 'Single Payment'),
        ('installment', 'Installment'),
        ('eft', 'Bank Transfer / EFT'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)

    # Common
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    installments = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # Card payment fields
    card_holder = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  # MM/YY
    cvv = models.CharField(max_length=4, blank=True, null=True)

    # EFT fields
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.payment_type} - {self.amount}₺"

    def clean(self):
        # Kredi kartı için gerekli alanlar
        if self.payment_type in ['single', 'installment']:
            if not all([self.card_holder, self.card_number, self.expiry_date, self.cvv]):
                raise ValidationError("Card information must be filled for card payments.")
            if self.payment_type == 'single' and self.installments != 1:
                raise ValidationError("Single payment must have 1 installment.")

        # EFT için gerekli alanlar
        elif self.payment_type == 'eft':
            if not all([self.sender_name, self.iban]):
                raise ValidationError("Sender name and IBAN must be provided for EFT.")
            if self.installments != 1:
                raise ValidationError("EFT must not have installments.")
