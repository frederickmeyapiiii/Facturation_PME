from django import forms
from .models import Invoice, Client, InvoiceLine, Payment

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': '06 12 34 56 78'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 3, 'placeholder': 'Adresse complète'}),
        }

class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'step': '0.01', 'min': '0', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
        }

InvoiceLineFormSet = forms.inlineformset_factory(
    Invoice, InvoiceLine, form=InvoiceLineForm, extra=1, can_delete=True
)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'client', 'tva_rate', 'status', 'date', 'due_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'number': forms.TextInput(attrs={'placeholder': 'EX: FAC-2026-001', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'client': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'tva_rate': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'value': '20.0', 'class': 'w-full px-3 py-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'step': '0.01', 'min': '0', 'placeholder': 'Montant'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 2, 'placeholder': 'Notes (optionnel)'}),
        }

