#!/usr/bin/env python
import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
django.setup()

from core.models import Company, Invoice

def create_sample_data():
    # Create a sample company
    company, created = Company.objects.get_or_create(
        name='Entreprise Demo',
        siret='12345678901234'
    )
    print(f"Company {'created' if created else 'already exists'}: {company.name}")

    # Create sample invoices
    invoices_data = [
        {'number': 'INV-001', 'client_name': 'Client A', 'amount_ht': 1000.00, 'status': 'PAID', 'date': date(2026, 1, 10)},
        {'number': 'INV-002', 'client_name': 'Client B', 'amount_ht': 2500.00, 'status': 'SENT', 'date': date(2026, 1, 12)},
        {'number': 'INV-003', 'client_name': 'Client C', 'amount_ht': 750.00, 'status': 'DRAFT', 'date': date(2026, 1, 14)},
        {'number': 'INV-004', 'client_name': 'Client D', 'amount_ht': 1800.00, 'status': 'SENT', 'date': date(2026, 1, 15)},
    ]

    for inv_data in invoices_data:
        invoice, created = Invoice.objects.get_or_create(
            company=company,
            number=inv_data['number'],
            defaults=inv_data
        )
        print(f"Invoice {'created' if created else 'already exists'}: {invoice.number} - {invoice.client_name}")

    print('Sample data creation completed!')

if __name__ == '__main__':
    create_sample_data()