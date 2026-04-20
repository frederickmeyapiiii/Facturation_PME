# Infrastructure as Code — Facturation PME

## Vue d'ensemble

Ce projet utilise **Ansible** pour automatiser le déploiement de l'application Facturation PME sur une infrastructure Ubuntu 22.04 LTS.
Ansible est un outil d'Infrastructure as Code (IaC) déclaratif qui permet de reproduire le déploiement de façon cohérente et idempotente.

## Fichiers Ansible

- `ansible/inventory.ini` : inventaire des serveurs
- `ansible/vars/main.yml` : variables de déploiement
- `ansible/deploy.yml` : playbook principal
- `ansible/templates/` : fichiers modèles (`.env`, `gunicorn.service`, `nginx.conf`)

## Structure

```
ansible/
├── inventory.ini           # Serveurs cible
├── deploy.yml              # Playbook
├── vars/
│   └── main.yml            # Variables
└── templates/
    ├── django_env.j2       # Fichier d'environnement Django
    ├── gunicorn.service.j2 # Service systemd Gunicorn
    └── nginx.conf.j2       # Configuration Nginx
```

## Prérequis

- Un serveur Ubuntu 22.04 LTS avec accès SSH
- Ansible installé sur votre machine locale
- La clé publique SSH prête pour l'authentification sans mot de passe

## Usage

### 1. Configurer l'inventaire

Modifier `ansible/inventory.ini` avec l'IP de votre serveur cible :

```ini
[web_servers]
facturation_pme_prod ansible_host=192.168.1.100 ansible_user=ubuntu
```

### 2. Adapter les variables

Éditer `ansible/vars/main.yml` pour changer :
- `django_secret_key` : clé secrète de production
- `db_password` : mot de passe base de données
- `django_allowed_hosts` : domaines autorisés

### 3. Exécuter le playbook

```bash
cd ansible
ansible-playbook -i inventory.ini deploy.yml
```

Pour un test en mode dry-run :

```bash
ansible-playbook -i inventory.ini deploy.yml --check
```

## Tâches effectuées par le playbook

1. **Mise à jour du système** : `apt update`
2. **Installation des dépendances** : Python 3, Nginx, PostgreSQL client, Git, etc.
3. **Création de l'utilisateur applicatif** : utilisateur système `facturation_pme`
4. **Clonage du dépôt** : depuis GitHub
5. **Configuration de l'environnement** : création du venv et installation des packages Python
6. **Génération du fichier `.env`** : variables d'environnement
7. **Migrations Django** : `python manage.py migrate`
8. **Collecte des fichiers statiques** : `python manage.py collectstatic`
9. **Configuration de Gunicorn** : service systemd
10. **Configuration de Nginx** : reverse proxy
11. **Sécurité** : enable UFW, ouvrir ports 22, 80, 443
12. **Vérification** : test de déploiement avec curl

## Idempotence

Le playbook est conçu pour être exécuté plusieurs fois sans risque d'erreur.
Chaque tâche est conçue pour être idempotente : relancer le playbook n'aura aucun effet secondaire.

## Mode de test

Pour tester le playbook localement avec Vagrant ou une VM :

```bash
# Créer un Vagrantfile avec une image Ubuntu 22.04
vagrant up

# Ajuster l'inventaire pour la VM locale
ansible-playbook -i inventory.ini --connection=local deploy.yml
```

## Notes

- Le playbook crée un utilisateur système `facturation_pme` sans droits interactifs.
- Gunicorn est lancé sous ce utilisateur avec un processus systemd.
- Nginx sert de reverse proxy, redirigeant les requêtes HTTP vers Gunicorn.
- En production, utiliser un certificat SSL/TLS valide sur Nginx.
- Pour les secrets (clés API, mots de passe), utiliser Ansible Vault :

```bash
ansible-vault encrypt ansible/vars/main.yml
```
