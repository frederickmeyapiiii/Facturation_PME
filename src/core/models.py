from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Brouillon'),
        ('SENT', 'Envoyée'),
        ('PAID', 'Payée'),
        ('OVERDUE', 'En retard'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=50)
    amount_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tva_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    @property
    def amount_ttc(self):
        return self.amount_ht * (1 + self.tva_rate / 100)

    @property
    def total_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def remaining_amount(self):
        return self.amount_ttc - self.total_paid

class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} x{self.quantity}"

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Paiement {self.amount} € - {self.invoice.number}"
