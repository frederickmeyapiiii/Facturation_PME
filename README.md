# Facturation PME

Application Django professionnelle de facturation pour une PME, déployée sur AWS avec CI/CD automatisé.

## Description

Ce projet gère la création, l'export CSV et la génération PDF de factures pour une entreprise.
Il permet de gérer les clients, les factures, les paiements et de suivre les statuts de facturation.

L'application est déployée automatiquement sur AWS EC2 via GitHub Actions CI/CD.

## Fonctionnalités

- **Page d'accueil professionnelle** avec présentation des fonctionnalités
- **Gestion des clients** : création, modification, suppression
- **Création de factures** avec lignes de facturation dynamiques
- **Modification de factures** existantes
- **Calcul automatique** du montant HT, TVA et TTC
- **Export des factures en CSV**
- **Génération de PDF de facture**
- **Suivi des statuts** : Brouillon, Envoyée, Payée, En retard
- **Gestion des paiements** avec historique
- **Authentification Django standard**
- **Dashboard** avec métriques financières

## Structure

- `src/finance_manager/` : configuration Django (settings, urls)
- `src/core/models.py` : modèles Company, Client, Invoice, InvoiceLine, Payment
- `src/core/views.py` : vues pour dashboard, factures, clients, paiements
- `src/core/forms.py` : formulaires Django
- `src/core/templates/core/` : templates HTML
- `docker/` : configuration Docker (Dockerfile, docker-compose files)
- `terraform/` : configuration Terraform pour AWS
- `.github/workflows/` : workflows GitHub Actions CI/CD
- `docs/` : documentation du projet

## Utilisation

### Démarrage local (développement)

```bash
cd src
python manage.py migrate
python create_superuser.py  # Crée un superuser admin/admin123 et une entreprise par défaut
python manage.py runserver
# Accès : http://localhost:8000/
# Dashboard : http://localhost:8000/dashboard/
# Admin Django : http://localhost:8000/admin/ (admin / admin123)
```

### Démarrage avec Docker

```bash
cd docker
docker compose up -d --build
# Page d'accueil : http://localhost:8000/
# Dashboard : http://localhost:8000/dashboard/
# Admin Django : http://localhost:8000/admin/ (admin / admin123)
# PostgreSQL sur port 5432
```

**Note** : Un superuser (`admin`/`admin123`) et une entreprise par défaut sont créés automatiquement au premier démarrage. Modifiez les credentials via les variables d'environnement dans `.env.example`.

### Démarrage avec monitoring (Prometheus + Grafana)

```bash
cd docker
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build
# Django : http://localhost:8000/
# Prometheus : http://localhost:9090
# Grafana : http://localhost:3000 (admin/admin)
```

### Déploiement sur AWS

Le déploiement est automatisé via GitHub Actions. À chaque push sur la branche `main` :

1. Les tests s'exécutent
2. L'image Docker est construite et pushée sur GitHub Container Registry
3. L'application est déployée automatiquement sur l'instance EC2 AWS

Pour configurer le déploiement, voir le dossier `terraform/` et le fichier `terraform/README.md`.

## Documentation

Voir le dossier `docs/` pour :
- `Documentation_Complete.md` : documentation complète du projet (regroupe tous les aspects techniques)

## Technologies utilisées

- **Backend** : Django 4.2.27
- **Base de données** : PostgreSQL 15
- **Containerisation** : Docker + Docker Compose
- **Génération PDF** : xhtml2pdf, weasyprint
- **Monitoring** : Prometheus + Grafana (optionnel)
- **Infrastructure** : Terraform (AWS)
- **CI/CD** : GitHub Actions
- **Hébergement** : AWS EC2
