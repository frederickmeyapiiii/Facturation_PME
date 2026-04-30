# Facturation PME

Application Django simple de facturation pour une PME.

## Description

Ce projet gère la création, l'export CSV et la génération PDF de factures pour une entreprise.
Il permet de gérer les clients, les factures, les paiements et de suivre les statuts de facturation.

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

### Test

```bash
cd docker
docker compose -f docker-compose.test.yml up -d
# Exécute les migrations et lance les tests
# Django disponible sur port 8001
```

## Documentation

Voir le dossier `docs/` pour :
- `Cahier_des_charges_Facturation_PME.md` : spécifications fonctionnelles et techniques
- `Architecture_Facturation_PME.md` : schéma technique et flux
- `Elements_Cles_Projet.md` : composants clés et choix d'architecture

## Technologies utilisées

- **Backend** : Django 4.2.27
- **Base de données** : PostgreSQL 16
- **Containerisation** : Docker + Docker Compose
- **Génération PDF** : xhtml2pdf, weasyprint
- **Monitoring** : Prometheus + Grafana (optionnel)
