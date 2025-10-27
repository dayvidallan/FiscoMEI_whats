
from django.contrib import admin
from .models import Plano, UsoMensal, MensagemLog, LancamentoEspelho

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ("nome","limite_mensal","preco")
    search_fields = ("nome",)

@admin.register(UsoMensal)
class UsoMensalAdmin(admin.ModelAdmin):
    list_display = ("user","mes","plano","mensagens","updated_at")
    search_fields = ("user__username","mes")

@admin.register(MensagemLog)
class MensagemLogAdmin(admin.ModelAdmin):
    list_display = ("telefone","user","tipo","created_at")
    search_fields = ("telefone","user__username")

@admin.register(LancamentoEspelho)
class LancamentoEspelhoAdmin(admin.ModelAdmin):
    list_display = ("user","tipo","valor_centavos","data","descricao")
    search_fields = ("user__username","descricao")
