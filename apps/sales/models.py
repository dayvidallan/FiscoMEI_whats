
from django.db import models
from decimal import Decimal

class Sale(models.Model):
    customer_name = models.CharField(max_length=120)
    product_name = models.CharField(max_length=120)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField()
    receipt_pdf = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date','-id']

    def __str__(self):
        return f'{self.customer_name} - {self.product_name} - {self.value} ({self.date})'
