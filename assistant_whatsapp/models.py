
from django.db import models
from django.conf import settings

class Plano(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    limite_mensal = models.PositiveIntegerField(default=200)
    preco = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class UsoMensal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usos_whatsapp")
    mes = models.CharField(max_length=7)  # YYYY-MM
    mensagens = models.PositiveIntegerField(default=0)
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "mes")

    def __str__(self):
        return f"{self.user} - {self.mes} - {self.mensagens} msgs"

class MensagemLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = models.CharField(max_length=32, db_index=True)
    tipo = models.CharField(max_length=20, default="text")  # text/image/audio
    conteudo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LancamentoEspelho(models.Model):
    """Fallback local quando não conseguimos criar no app finance.
    Serve como espelho para posterior sincronização manual.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=(("entrada","Entrada"),("saida","Saída")))
    valor_centavos = models.IntegerField()
    descricao = models.TextField(blank=True)
    data = models.DateField()
    origem = models.CharField(max_length=120, blank=True)
    cpf_cnpj = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
