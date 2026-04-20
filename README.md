# Facturation PME

Application Django simple de facturation pour une seule entreprise.

## Description

Ce projet gère la création, l'export CSV et la génération PDF de factures pour une unique société.
Il conserve une seule entreprise dans le système et supprime l'ancienne orientation multi-entreprises pour se concentrer sur la facturation PME.

## Fonctionnalités

- Création de factures
- Calcul automatique du montant TTC
- Export des factures en CSV
- Génération de PDF de facture
- Authentification Django standard

## Structure

- `src/finance_manager/urls.py` : routes principales
- `src/core/models.py` : modèle `Company` et `Invoice`
- `src/core/views.py` : gestion du dashboard et des exports
- `src/core/templates/core/` : interface de facturation
- `docker-compose.yml` et `Dockerfile` : configuration Docker pour un environnement PostgreSQL
- `docker-compose.monitoring.yml` : stack Prometheus + Grafana pour la supervision
- `ansible/` : playbook Ansible pour déploiement automatisé sur serveur Ubuntu
- `.github/workflows/ci.yml` : pipeline CI GitHub Actions pour checks, tests et build Docker
- `docs/Architecture_Facturation_PME.md` : schéma d'architecture technique du projet
- `docs/IaC_Ansible_Facturation_PME.md` : guide de déploiement avec Infrastructure as Code
- `docs/Monitoring_Facturation_PME.md` : configuration et utilisation du monitoring Prometheus + Grafana
- `docs/` : documentation du projet (CDC, analyse préliminaire, sécurité, env de test)

## Utilisation

### Démarrage local (développement)

```bash
cd src
python manage.py migrate
python manage.py runserver
# Accès : http://localhost:8000/dashboard/
```

### Démarrage avec Docker

```bash
docker compose up -d --build
# Django : http://localhost:8000/dashboard/
# PostgreSQL sur port 5432
```

### Démarrage avec monitoring (Prometheus + Grafana)

```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build
# Django : http://localhost:8000/dashboard/
# Prometheus : http://localhost:9090
# Grafana : http://localhost:3000 (admin/admin)
```

### Test

```bash
docker compose -f docker-compose.test.yml up -d
# Exécute les migrations et lance les tests
# Django disponible sur port 8001
```

### Déploiement en production (Ansible)

```bash
cd ansible
docker compose run ansible -i inventory.ini deploy.yml
```

## Documentation

Voir le dossier `docs/` pour :
- `Cahier_des_charges_Facturation_PME.md` : spécifications fonctionnelles et techniques
- `Architecture_Facturation_PME.md` : schéma technique et flux
- `Elements_Cles_Projet.md` : composants clés et choix d'architecture
- `IaC_Ansible_Facturation_PME.md` : déploiement automatisé
- `Monitoring_Facturation_PME.md` : supervision et métriques
- `Securiser_Infrastructure_Facturation_PME.md` : sécurité et infrastructure
- `Environnement_de_test_Facturation_PME.md` : stratégies de test

## Compétences couvertes

- **CP1** : Provisionnement serveur avec scripts Bash
- **CP2** : Infrastructure as Code (Ansible)
- **CP3** : Containerisation (Docker + Docker Compose)
- **CP4** : CI/CD (GitHub Actions)
- **CP5** : Environnements isolés (test, pré-prod, production)
- **CP7/CP8** : Gestion de version et publication (Git/GitHub)
- **CP9/CP10** : Documentation technique complète
