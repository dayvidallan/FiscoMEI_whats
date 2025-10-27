
from django.db import models
class Transaction(models.Model):
    KIND_CHOICES = [('IN','Entrada'),('OUT','Saída')]
    kind = models.CharField(max_length=3, choices=KIND_CHOICES, default='IN')
    date = models.DateField()
    category = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-date','-id']
    def __str__(self): return f"{self.get_kind_display()} - {self.date} - {self.amount}"


class Company(models.Model):
    name = models.CharField(max_length=120, default='Minha Empresa')
    document = models.CharField(max_length=32, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    def __str__(self): return self.name
