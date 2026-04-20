# Éléments clés du projet — Facturation PME

## Vue d'ensemble

Ce document résume les composants et choix clés du projet Facturation PME, une application Django de gestion de factures pour une entreprise unique.

## Positionnement client

Le projet adresse le besoin d'une PME souhaitant moderniser sa gestion de facturation :
- Gestion manuelle actuelle : tableurs, erreurs de saisie, manque de centralisation
- Solution proposée : application web Django permettant la création, le suivi et l'export des factures
- Utilisateurs : administrateur (expert) et assistant (gérant quotidien)

## Architecture technique

Stack :
- **Framework** : Django 4.2 avec Python 3.14
- **Base de données** : PostgreSQL (production) / SQLite (développement)
- **Déploiement** : Docker + Ansible
- **Monitoring** : Prometheus + Grafana
- **CI/CD** : GitHub Actions

Séparation des rôles :
- `admin` : portail d'administration système
- `assistant` : dashboard de facturation
- Contrôle d'accès par vues Django (PermissionDenied sur accès non autorisé)

## Sécurité

Mesures implémentées :
- Authentification Django standard (login/password)
- Séparation des interfaces par rôle utilisateur
- Configuration d'environnement : `SECRET_KEY` et `DEBUG` chargés depuis variables `DJANGO_*`
- Pare-feu UFW + SSH sécurisé documentés dans `docs/Securiser_Infrastructure_Facturation_PME.md`
- Configuration `ALLOWED_HOSTS` restrictive

## Environnements

Trois niveaux de déploiement :
- **Test** : `docker-compose.test.yml` avec PostgreSQL isolé
- **Pré-production** : miroir fonctionnel pour validation
- **Production** : déploiement via Ansible, configuration Nginx + Gunicorn

## Automatisation

Scripts et outils :
- **Provisionnement** : `scripts/provision/provision-web-server.sh` (systèmes, dépendances, configuration)
- **Tests** : `scripts/provision/check-test-env.sh` et `scripts/provision/check-web-server.sh`
- **Backup** : `scripts/backup_db.sh` (support PostgreSQL + SQLite)
- **Playbook Ansible** : `ansible/deploy.yml` pour déploiement complet
- **Pipeline CI/CD** : `.github/workflows/ci.yml` pour tests et build Docker

## Livrables

Code source :
- Application Django dans `src/` avec modèles `Company` et `Invoice`
- Templates HTML : dashboard, login, PDF export
- Exports : CSV et PDF pour les factures

Infrastructure :
- Dockerfile pour containerisation Django
- Docker Compose configurations (dev, test, monitoring)
- Playbook Ansible pour infrastructure as code
- Scripts de provisionnement Bash

Documentation :
- Cahier des charges : `docs/Cahier_des_charges_Facturation_PME.md`
- Architecture : `docs/Architecture_Facturation_PME.md` + schéma SVG
- Sécurité : `docs/Securiser_Infrastructure_Facturation_PME.md`
- Test : `docs/Environnement_de_test_Facturation_PME.md`
- IaC : `docs/IaC_Ansible_Facturation_PME.md`
- Monitoring : `docs/Monitoring_Facturation_PME.md`
- Analyse préliminaire : `docs/Analyse_Preliminaire_Facturation_PME.md`

## État du projet

Le projet est opérationnel, documenté et prêt pour déploiement sur infrastructure Ubuntu 22.04 LTS.
La séparation entre les trois environnements (test, pré-prod, prod) est entièrement implémentée et tracée.
