# Présentation orale — Facturation PME

## 1. Objectif

Ce document propose des conseils pour préparer et présenter oralement le projet de facturation PME devant le jury.
Il complète le dossier technique en expliquant comment structurer ton discours et quelles preuves mettre en avant.

## 2. Structure recommandée

### 2.1 Introduction (1 min)
- Présente rapidement le client fictif : une PME qui a besoin d’un outil simple de facturation.
- Explique le problème : gestion manuelle, erreurs, manque de centralisation et difficulté à suivre les paiements.
- Donne l’objectif : déployer une application Django qui permet de gérer les factures d’une entreprise unique.

### 2.2 Architecture et stack (1 min)
- Montre la stack technique : Django, Python, SQLite en local, scripts Bash, documentation et Git.
- Évoque l’architecture simple : application web, base de données, authentification et séparation des rôles.
- Si tu as un schéma, décris-le rapidement.

### 2.3 Sécurité et infrastructure (1 min)
- Explique les principaux choix de sécurité : SSH sécurisé, pare-feu, certificats TLS, protection des accès.
- Dis que tu as documenté ces choix dans `docs/Securiser_Infrastructure_Facturation_PME.md`.
- Parle de la vérification : tests de santé, déploiement validé avant production.

### 2.4 Environnements et tests (1 min)
- Présente l’environnement de test : fichier `docker-compose.test.yml` et script de vérification `scripts/provision/check-test-env.sh`.
- Explique la différence entre test, pré-prod et prod : isolation des données, parité fonctionnelle, pipeline progressif.
- Dis que le jury peut consulter `docs/Environnement_de_test_Facturation_PME.md` pour les détails.

### 2.5 Conclusion et points forts
- Résume les réalisations : fonctionnalité, sécurité, documentation, automatisation.
- Mentionne les livrables disponibles : code dans `src/`, documentation dans `docs/`, scripts dans `scripts/provision/`.
- Termine sur une phrase positive : « Le projet est opérationnel, documenté et pensé pour être maintenable. »

## 3. Conseils de style oral

- Parle lentement, avec des phrases courtes.
- Utilise des mots simples et concrets.
- Montre du doigt le schéma ou le fichier quand tu expliques.
- Ne lis pas un texte mot à mot.
- Si tu hésites, reste factuel et renvoie au dossier technique.

## 4. Ce que le jury cherche

### 4.1 Clarté
- Comprendre rapidement le besoin et la solution.
- Voir que le projet a une logique cohérente.

### 4.2 Preuves
- S’assurer qu’il y a des documents clairs et des fichiers concrets.
- Vérifier que tu ne parles pas seulement de choses théoriques.

### 4.3 Réalisme
- Montrer que le projet est faisable et qu’il est prêt à être expliqué.
- Éviter les promesses vagues.

## 5. Ce qu’il faut éviter de dire

- « C’est un rendu du prof ».
- « Je n’ai pas eu le temps de… » (sauf si c’est très bref et orienté futur).
- Des détails techniques inutiles qui n’apportent rien au jury.
- Des expressions trop familières.

## 6. Exemples de phrases utiles

- « Le projet est un outil de facturation pour aider une PME à gérer ses factures et sa trésorerie. »
- « J’ai structuré la solution en séparant l’accès admin et l’accès assistant. »
- « J’ai documenté le cahier des charges, la sécurité, l’automatisation et l’environnement de test. »
- « Le dossier contient des preuves concrètes : fichiers de configuration, scripts et explications. »

## 7. Comment utiliser ce document

- Prépare une présentation courte basée sur ces points.
- Ouvre le dossier `docs/` si le jury veut voir les preuves.
- Si le jury pose une question, réponds avec le document correspondant : sécurité, test, automation.
