# Environnement de test – Facturation PME

## 1. Objectif

Ce document décrit l’environnement de test du projet de facturation PME, en lien avec le référentiel BC02-CP5.
Il montre que l’application dispose d’un environnement distinct de la production et d’une configuration versionnée dédiée au test.

## 2. Contexte et exigences
BC02-CP5 demande :
- Créer un environnement de test conforme au cahier des charges.
- Effectuer les premiers tests.
- Faire remonter les dysfonctionnements à l’équipe de développement.

> Le critère du jury est : « l’environnement de tests est conforme au cahier des charges ». Il faut donc décrire l’environnement dans le CDC et le matérialiser dans le dépôt.

## 3. Les trois environnements du projet

### 3.1 Environnement de test
- Objectif : valider le code sur une configuration isolée avant toute mise en pré-production.
- Isolation : base de test séparée, variables d’environnement spécifiques, port dédié, volume de données distinct.
- Entrée en jeu : développeurs et pipeline CI.

### 3.2 Environnement de pré-production
- Objectif : vérifier le déploiement avec une configuration fonctionnellement proche de la production.
- Mêmes images, même pipeline, mêmes fichiers de déploiement.
- Différences acceptables : taille d’instance réduite, domaine `preprod.facturation-pme.local` ou `preprod.local`.

### 3.3 Environnement de production
- Objectif : service final pour les utilisateurs.
- Données réelles, monitoring actif, déploiement automatisé conservateur.
- Déploiement autorisé uniquement après validation du test et de la pré-production.

## 4. Ce que « isolé » veut dire pour Facturation PME

### Isolation réseau
- Le test ne doit pas dépendre de la base de production.
- Les services de test utilisent un port distinct et un réseau dédié.

### Isolation des données
- La base de données de test est indépendante.
- Les fixtures ou jeux de données peuvent être simples et reproductibles.
- Pas de données personnelles réelles dans les environnements de test.

### Isolation des secrets
- Les variables d’environnement de test ne doivent pas contenir de clés de production.
- Les secrets de test peuvent être plus légers, mais ils ne donnent accès à rien de réel.

## 5. Preuve dans le dépôt

### 5.1 Fichier de configuration dédié au test
Le dépôt contient maintenant un fichier versionné :
- `docker-compose.test.yml`

Ce fichier matérialise l’environnement de test et montre au jury qu’un environnement distinct est prévu.

### 5.2 Script de vérification smoke test
Le dépôt contient également :
- `scripts/provision/check-test-env.sh`

Ce script illustre un test minimal automatisé dans l’environnement de test.

## 6. Proposition de pipeline simple

Un pipeline CI/CD conforme à CP5 peut ressembler à :

- `deploy_test` : déployer dans l’environnement de test avec `docker compose -f docker-compose.test.yml up -d`
- `validate` : exécuter un smoke test avec `./scripts/provision/check-test-env.sh`
- `deploy_preprod` : si le test passe, déployer en pré-production
- `deploy_prod` : si la pré-prod passe, déployer en production

Ce processus rend explicite la valeur de la phase de test et évite un déploiement sans validation.

## 7. Schéma attendu pour le jury

Le jury doit pouvoir lire clairement :
- un environnement `test` séparé,
- un environnement `pré-production` miroir fonctionnel de la production,
- un environnement `production` final.

Un schéma simple doit montrer :

[Pipeline CI/CD] → [Env. Test] → [Pré-prod] → [Prod]

Avec des bases de données distinctes et des services isolés.

## 8. Ce qui différencie test / pré-prod / prod

### Identique
- même application Django,
- même processus de déploiement,
- même structure de variables d’environnement,
- mêmes images ou mêmes packages.

### Différent
- taille ou ressources du serveur,
- domaine ou URL,
- données anonymisées ou synthétiques en test/pré-prod,
- volume de stockage dédié en test.

## 9. Pièges à éviter

- Ne pas utiliser le laptop de développement comme environnement de test.
- Ne pas se contenter d’une seule variable `NODE_ENV=test` sur le même environnement.
- Ne pas stocker de secrets de production dans le fichier de test.
- Ne pas écrire un stage `deploy_test` sans exécuter de test automatique.

## 10. Consignes pour la suite

1. Ajouter un paragraphe « Environnements » dans le CDC si ce n’est pas déjà fait.
2. Conserver `docker-compose.test.yml` comme preuve de la configuration test.
3. Ajouter un smoke test dans le pipeline ou dans la documentation de build.
4. Mettre à jour le schéma d’architecture pour représenter `test`, `pré-prod` et `prod` comme trois niveaux séparés.
