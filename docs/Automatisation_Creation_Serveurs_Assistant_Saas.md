# Automatisation création de serveurs – Assistant Saas

## 1. Objectif

Ce document présente l’automatisation de la création et de la configuration d’un serveur virtuel pour le projet **Assistant Saas**.
Il explique les choix techniques, les scripts produits et les vérifications mises en place pour rendre l’infrastructure reproductible.

Ce document fait partie du dossier de projet et est destiné à être lu par le jury et l’équipe pédagogique.

## 2. Contexte

Un serveur créé manuellement n’est pas reproductible et ne peut pas être remis en l’état en cas de panne.
Le projet Assistant Saas doit montrer qu’un serveur peut être créé et configuré automatiquement avec un script, puis vérifié et documenté.

## 3. Ce que le jury attend

Le jury vérifie que :
- le serveur est fonctionnel après exécution du script,
- la configuration est conforme au cahier des charges,
- la documentation est mise à jour.

La compétence CP1 évalue la capacité à écrire un script de création de serveur, à automatiser sa configuration, à vérifier son bon fonctionnement et à documenter le travail.

## 4. Scripts produits

### 4.1 Script Bash principal

Fichier : `scripts/provision/provision-web-server.sh`

Rôle : créer et configurer un serveur Linux Ubuntu pour héberger l’application Django.

Fonctionnalités attendues :
- mise à jour du système,
- installation des paquets nécessaires (Nginx, Git, UFW, Python, etc.),
- création d’un utilisateur dédié,
- configuration de Nginx en reverse proxy,
- configuration du pare-feu local (UFW),
- vérification de l’état des services.

### 4.2 Script de vérification

Fichier : `scripts/provision/check-web-server.sh`

Rôle : vérifier que le serveur est opérationnel après le provisionnement.

Vérifications attendues :
- Nginx en service,
- UFW actif,
- port web ouvert,
- application accessible localement.

## 5. Bonnes pratiques du script

### 5.1 En-tête et métadonnées

Chaque script doit commencer par un en-tête clair :
- description,
- usage,
- auteur,
- date.

### 5.2 Options de sécurité

Utiliser :
```bash
set -euo pipefail
```
- `-e` : arrêter le script si une commande échoue,
- `-u` : erreur si une variable n’est pas définie,
- `-o pipefail` : erreur si une commande dans un pipe échoue.

### 5.3 Idempotence

Le script doit pouvoir être exécuté plusieurs fois sans provoquer d’erreur ni de changement non prévu.
Par exemple, ne pas recréer un utilisateur s’il existe déjà.

### 5.4 Journalisation

Le script doit écrire un journal horodaté, par exemple dans `/var/log/provision-web-server.log`.

### 5.5 Vérification finale

Le script doit vérifier le résultat de l’installation et retourner une erreur si un service n’est pas actif.

## 6. Exemple de démarche technique

Pour chaque script, documenter :
- le problème résolu,
- les choix techniques (`set -euo pipefail`, idempotence, ordre des opérations),
- les tests effectués,
- les difficultés rencontrées.

## 7. Correspondance avec CP1

Ce document montre que tu maîtrises :
- la création d’un script Bash pour provisionner un serveur,
- l’automatisation de la configuration,
- la vérification de l’état du serveur,
- la documentation de la réalisation.

## 8. Où mettre ce document ?

- Dans `docs/Automatisation_Creation_Serveurs_Assistant_Saas.md`.
- Dans le dossier final, le jury doit pouvoir trouver :
  - `docs/Cahier_des_charges_Assistant_Saas.md`,
  - `docs/Securiser_Infrastructure_Assistant_Saas.md`,
  - `docs/Automatisation_Creation_Serveurs_Assistant_Saas.md`,
  - `scripts/provision/provision-web-server.sh`,
  - `scripts/provision/check-web-server.sh`.

## 9. Conseils pour l’oral

- Explique que le script rend le serveur reproductible.
- Montre que le script est la documentation de la création du serveur.
- Explique pourquoi tu utilises `set -euo pipefail` et l’idempotence.
- Précise comment tu testes le résultat.
