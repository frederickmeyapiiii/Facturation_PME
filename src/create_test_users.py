#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile, Company

def create_test_users():
    # Récupérer l'entreprise existante
    company = Company.objects.first()
    print(f'Entreprise disponible: {company.name}')

    # Créer un utilisateur GÉRANT
    gerant_user, created = User.objects.get_or_create(
        username='gerant',
        defaults={
            'email': 'gerant@example.com',
            'first_name': 'Jean',
            'last_name': 'Dupont'
        }
    )
    if created:
        gerant_user.set_password('gerant123')
        gerant_user.save()

    gerant_profile, created = Profile.objects.get_or_create(
        user=gerant_user,
        defaults={
            'company': company,
            'role': 'GERANT'
        }
    )
    print(f'Gérant créé: {gerant_user.username} - {gerant_profile.get_role_display()}')

    # Créer un utilisateur COLLABORATEUR
    collab_user, created = User.objects.get_or_create(
        username='collab',
        defaults={
            'email': 'collab@example.com',
            'first_name': 'Marie',
            'last_name': 'Martin'
        }
    )
    if created:
        collab_user.set_password('collab123')
        collab_user.save()

    collab_profile, created = Profile.objects.get_or_create(
        user=collab_user,
        defaults={
            'company': company,
            'role': 'COLLAB'
        }
    )
    print(f'Collaborateur créé: {collab_user.username} - {collab_profile.get_role_display()}')

    # Créer un utilisateur EXPERT supplémentaire (sans entreprise)
    expert_user, created = User.objects.get_or_create(
        username='expert',
        defaults={
            'email': 'expert@example.com',
            'first_name': 'Pierre',
            'last_name': 'Dubois'
        }
    )
    if created:
        expert_user.set_password('expert123')
        expert_user.save()

    expert_profile, created = Profile.objects.get_or_create(
        user=expert_user,
        defaults={
            'company': None,  # Pas d'entreprise assignée
            'role': 'EXPERT'
        }
    )
    print(f'Expert créé: {expert_user.username} - {expert_profile.get_role_display()}')

if __name__ == '__main__':
    create_test_users()