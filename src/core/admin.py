from django.contrib import admin
from .models import Company, Invoice, AuditLog

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'siret', 'created_at')
    search_fields = ('name', 'siret')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    # On affiche les colonnes importantes dans la liste
    list_display = ('number', 'company', 'client_name', 'amount_ht', 'status', 'date')
    # On ajoute des filtres sur le côté pour le comptable
    list_filter = ('status', 'company', 'date')
    # On permet la recherche par numéro de facture ou client
    search_fields = ('number', 'client_name')
    # Organisation par date
    date_hierarchy = 'date'

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'timestamp')
    readonly_fields = ('action', 'user', 'timestamp') # On ne peut pas modifier un log !