from django.contrib import admin
from .models import Company, Client, Invoice, InvoiceLine, Payment

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'siret', 'created_at')
    search_fields = ('name', 'siret')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'company', 'client', 'amount_ht', 'amount_ttc', 'status', 'date')
    list_filter = ('status', 'company', 'date')
    search_fields = ('number', 'client__name')
    date_hierarchy = 'date'
    readonly_fields = ('amount_ttc', 'total_paid', 'remaining_amount')

@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'total')
    list_filter = ('invoice',)
    search_fields = ('description', 'invoice__number')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'date', 'notes')
    list_filter = ('date', 'invoice')
    search_fields = ('invoice__number', 'notes')
