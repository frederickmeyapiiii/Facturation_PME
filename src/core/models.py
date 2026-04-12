from django.db import models
from django.contrib.auth.models import User

# 1. Pour gérer le multi-entreprises (SaaS)
class Company(models.Model):
    name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. Pour la gestion des factures
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

# 3. Pour le Reporting (Audit Trail)
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# 4. Profil Utilisateur Étendu
class Profile(models.Model):
    ROLE_CHOICES = [
        ('EXPERT', 'Expert Comptable (Cabinet)'),
        ('GERANT', 'Gérant PME'),
        ('COLLAB', 'Collaborateur PME'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='GERANT')

    def __str__(self):
        return f"{self.user.username} - {self.role} ({self.company.name if self.company else 'Cabinet'})"