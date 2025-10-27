
from django.db import models
class MEI(models.Model):
    owner_name = models.CharField('Nome do titular', max_length=120)
    cpf = models.CharField('CPF', max_length=14, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    trade_name = models.CharField('Nome fantasia', max_length=120, blank=True)
    corporate_name = models.CharField('Razão social', max_length=180, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField('Endereço', max_length=200, blank=True)
    city = models.CharField('Cidade', max_length=80, blank=True)
    state = models.CharField('UF', max_length=2, blank=True)
    cep = models.CharField('CEP', max_length=9, blank=True)
    im = models.CharField('Inscrição Municipal', max_length=40, blank=True)
    ie = models.CharField('Inscrição Estadual', max_length=40, blank=True)
    regime = models.CharField('Regime Tributário', max_length=50, default='SIMEI')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: verbose_name='MEI'; verbose_name_plural='MEIs'
    def __str__(self): return f"{self.trade_name or self.owner_name} ({self.cnpj})"
