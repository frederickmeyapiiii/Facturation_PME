# Cahier des charges – Facturation PME

## 1. Contexte et besoin client

Client : une PME souhaitant moderniser sa gestion de facturation.

Situation initiale :
- L’entreprise gère ses factures avec des tableurs et des échanges manuels.
- Les factures ne sont pas centralisées et il est difficile de suivre les statuts de paiement.
- Le dirigeant veut une interface simple pour créer, consulter et exporter les factures.

Problème / déclencheur :
- Les erreurs de saisie se multiplient, les relances sont difficiles et les rapports sont incomplets.
- L’entreprise souhaite un outil fiable pour gérer ses factures et exporter les données rapidement.
- Il faut un accès sécurisé, une interface de création de facture et un export simple.

Objectif attendu :
- Déployer une application web de facturation pour une seule entreprise.
- Offrir une interface de dashboard pour créer et suivre les factures.
- Permettre l’export des factures en CSV et la génération de PDF.

## 2. Périmètre fonctionnel

Services à déployer :
- Application web Django pour la gestion des factures d’une entreprise unique.
- Authentification des utilisateurs.
- Rôles séparés : `admin` (expert/backstage) et `assistant` (gérant/dashboard).
- Dashboard entreprise pour les gérants avec consultation et création des factures.
- Portail admin pour superviser les factures et les données globales.

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

## 3.1 Environnements projet

- **Test** : environnement isolé pour valider les premières corrections. Il doit disposer d’une configuration dédiée versionnée dans le dépôt (`docker-compose.test.yml`).
- **Pré-production** : miroir fonctionnel de la production, utilisant le même processus de déploiement et les mêmes images/logiques.
- **Production** : service final pour les utilisateurs.

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
- Cahier des charges (`docs/Cahier_des_charges_Facturation_PME.md`).
- Spécifications techniques (architecture, stack, diagramme simple).
- Dossier de projet avec captures d’écran et explications.
- Présentation / diaporama expliquant le contexte, l’architecture et les réalisations.

### Compétences couvertes
- **CP1 / CP3** : mise en place de l’application web et de l’infrastructure de développement.
- **CP4** : sécurité des accès et séparation des rôles.
- **CP7 / CP8** : gestion des containers/environnement et publication via Git.
- **CP9 / CP10** : documentation et preuve de fonctionnement.
