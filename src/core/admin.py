from django.contrib import admin
from .models import Company, Invoice

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'siret', 'created_at')
    search_fields = ('name', 'siret')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'company', 'client_name', 'amount_ht', 'status', 'date')
    list_filter = ('status', 'company', 'date')
    search_fields = ('number', 'client_name')
    date_hierarchy = 'date'
