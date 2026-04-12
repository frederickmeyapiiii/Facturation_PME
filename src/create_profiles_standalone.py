#!/usr/bin/env python3
import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')

try:
    django.setup()
except Exception as e:
    print(f"Erreur Django setup: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from core.models import Profile, Company

def main():
    try:
        # Récupérer l'entreprise
        company = Company.objects.first()
        if not company:
            print("Création entreprise...")
            company = Company.objects.create(name="Entreprise Test", address="123 Rue Test")
            print(f"Entreprise créée: {company.name}")

        print(f"Entreprise trouvée: {company.name} (ID: {company.id})")

        # Créer les utilisateurs de test
        users_data = [
            ('gerant', 'GERANT', company),
            ('collab', 'COLLAB', company),
            ('expert', 'EXPERT', None),
        ]

        for username, role, comp in users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(f'{username}123')
                user.save()
                print(f"Utilisateur créé: {username}")

            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'role': role, 'company': comp}
            )
            if created:
                print(f"Profil créé pour {username}: {profile.get_role_display()}")
            else:
                print(f"Profil existant pour {username}: {profile.get_role_display()}")

        print("\n=== RÉSUMÉ DES PROFILS ===")
        for user in User.objects.all():
            try:
                profile = user.profile
                company_name = profile.company.name if profile.company else 'AUCUNE'
                print(f"{user.username}: {profile.get_role_display()} - Entreprise: {company_name}")
            except Profile.DoesNotExist:
                print(f"{user.username}: AUCUN PROFIL")

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()