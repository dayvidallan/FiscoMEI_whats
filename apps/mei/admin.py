from django.contrib import admin
from .models import MEI
@admin.register(MEI)
class MEIAdmin(admin.ModelAdmin):
    list_display=('owner_name','trade_name','cnpj','email','phone','created_at')
    search_fields=('owner_name','trade_name','cnpj','cpf')
