from django.contrib import admin
from .models import Transaction, Company
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=('date','kind','category','amount','created_at')
    list_filter=('kind','date')
    search_fields=('description','category')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display=('name','document')
