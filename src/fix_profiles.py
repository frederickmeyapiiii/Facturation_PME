#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile, Company

company = Company.objects.get(id=2)  # Boulangerie Soleil

corrections = {
    'gerant': ('GERANT', company),
    'collab': ('COLLAB', company),
    'expert': ('EXPERT', None),
}

for username, (role, comp) in corrections.items():
    user = User.objects.get(username=username)
    profile = user.profile
    profile.role = role
    profile.company = comp
    profile.save()
    company_name = comp.name if comp else 'AUCUNE'
    print(f'{username}: {profile.get_role_display()} - {company_name}')

print('\n=== ÉTAT FINAL ===')
for user in User.objects.all():
    try:
        profile = user.profile
        company_name = profile.company.name if profile.company else 'AUCUNE'
        print(f'{user.username}: {profile.get_role_display()} - {company_name}')
    except:
        print(f'{user.username}: AUCUN PROFIL')