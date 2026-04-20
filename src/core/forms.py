from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        # On ne demande pas la 'company' car elle sera ajoutée automatiquement
        fields = ['number', 'client_name', 'amount_ht', 'tva_rate', 'status', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'number': forms.TextInput(attrs={'placeholder': 'EX: FAC-2026-001', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'client_name': forms.TextInput(attrs={'placeholder': 'Nom du client', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'amount_ht': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'tva_rate': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'value': '20.0', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

