#!/usr/bin/env python
"""Script pour créer un superuser Django et une entreprise par défaut automatiquement."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Company

User = get_user_model()

# Configuration du superuser (peut être surchargé via variables d'environnement)
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Création du superuser
if not User.objects.filter(username=username).exists():
    print(f"[INIT] Creating superuser: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"[INIT] Superuser '{username}' created successfully! (password: {password})")
else:
    print(f"[INIT] Superuser '{username}' already exists.")

# Création d'une entreprise par défaut si aucune n'existe
if not Company.objects.exists():
    print("[INIT] Creating default company...")
    Company.objects.create(
        name="NAYOMI",
        siret="12345678901234"
    )
    print("[INIT] Default company created: 'NAYOMI' (SIRET: 12345678901234)")
else:
    print(f"[INIT] Company already exists: {Company.objects.first().name}")
