# Cahier des charges – Assistant Saas

## 1. Contexte et besoin client

Client : une PME de services comptables fictive nommée **Assistant Saas**.

Situation initiale :
- L’entreprise gère ses factures et ses clients avec des fichiers Excel et des échanges manuels.
- Les collaborateurs n’ont pas de portail centralisé pour suivre les factures.
- Les accès sont partagés et il n’y a pas de séparation claire des rôles.

Problème / déclencheur :
- Les erreurs augmentent, les factures sont mal suivies, et les gérants perdent du temps.
- Le service comptable souhaite un outil fiable pour gérer les clients, les sociétés et les factures.
- Il faut aussi un accès sécurisé pour l’administrateur et une interface dédiée pour les gérants.

Objectif attendu :
- Déployer une application web de gestion de facturation nommée **Assistant Saas**.
- Offrir une interface **admin** pour la supervision et une interface **dashboard** pour les gérants.
- Permettre la gestion des sociétés, des utilisateurs et des factures avec authentification.

## 2. Périmètre fonctionnel

Services à déployer :
- Application web Django pour la gestion des sociétés et des factures.
- Authentification des utilisateurs.
- Rôles séparés : `admin` (expert/backstage) et `assistant` (gérant/dashboard).
- Dashboard entreprise pour les gérants avec consultation et création des factures.
- Portail admin pour superviser les sociétés et les données globales.

Applications et utilisateurs :
- Application principale située dans le dossier `src/`.
- Utilisateurs du projet :
  - `admin` : chargé de l’administration et de la surveillance.
  - `assistant` : chargé de la gestion quotidienne des factures.

## 3. Contraintes techniques

- **Infrastructure cible** : projet conçu pour un déploiement sur une infrastructure cloud ou serveur Linux.
- **OS cible** : compatible avec Linux Ubuntu 22.04 LTS en production, développement possible sous Windows.
- **Version** : application basée sur Django 4.2 et Python 3.14.
- **Compatibilité** : le code doit pouvoir être exécuté localement avec un environnement virtuel Python.

## 4. Contraintes de sécurité

- **Authentification** : l’accès à l’application doit être sécurisé par un login/mot de passe.
- **Séparation des rôles** : un `admin` ne doit pas utiliser la même interface qu’un `assistant`.
- **Secrets** : aucun secret ou mot de passe ne doit être stocké en clair dans le dépôt.
- **Accès non autorisé** : les pages interdites doivent renvoyer une erreur 403.

## 5. Contraintes d’exploitation / monitoring

- **Disponibilité** : l’application doit être utilisable et testable localement pour la démonstration.
- **Supervision** : le dossier doit inclure des preuves de fonctionnement (captures d’écran, tests, descriptions).
- **Journalisation** : les actions importantes doivent pouvoir être expliquées dans le dossier de projet.

## 6. Livrables attendus

- Code source du projet sur GitHub.
- Cahier des charges (`docs/Cahier_des_charges_Assistant_Saas.md`).
- Spécifications techniques (architecture, stack, diagramme simple).
- Dossier de projet avec captures d’écran et explications.
- Présentation / diaporama expliquant le contexte, l’architecture et les réalisations.

### Compétences couvertes
- **CP1 / CP3** : mise en place de l’application web et de l’infrastructure de développement.
- **CP4** : sécurité des accès et séparation des rôles.
- **CP7 / CP8** : gestion des containers/environnement et publication via Git.
- **CP9 / CP10** : documentation et preuve de fonctionnement.

## 7. Où mettre ce document ?

- Place ce fichier dans le dossier `docs/` de ton projet.
- Dans le dossier de projet final, tu peux inclure aussi :
  - `README.md`
  - `docs/Analyse_Preliminaire.md`
  - `docs/Cahier_des_charges_Assistant_Saas.md`
  - le code source dans `src/`
- Le jury pourra lire `docs/Cahier_des_charges_Assistant_Saas.md` comme ton CDC.

## 8. Conseils pour l’oral

- Présente vite le client, le problème et l’objectif.
- Explique ensuite les 3 contraintes : cloud, sécurité, monitoring.
- Dis que tu as réalisé le projet en local, mais que les choix sont pensés pour un déploiement cloud.
- Garder 3 à 5 minutes pour le CDC dans ton diaporama.
