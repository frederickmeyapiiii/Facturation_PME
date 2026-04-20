from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Brouillon'),
        ('SENT', 'Envoyée'),
        ('PAID', 'Payée'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=255)
    amount_ht = models.DecimalField(max_digits=10, decimal_places=2)
    tva_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    date = models.DateField()

    @property
    def amount_ttc(self):
        return self.amount_ht * (1 + self.tva_rate / 100)
