Livrable 1 : Analyse Préliminaire - Facturation PME

1. Introduction et Contexte
Client : une PME qui a besoin d’un système de facturation simple et centralisé.

Cible : une seule entreprise souhaitant gérer ses factures sans complexité.

Problématique : Actuellement, l’entreprise utilise des outils hétérogènes (Excel, logiciels obsolètes, papier). Cela entraîne une perte de temps pour le dirigeant et des erreurs dans le suivi des factures.

Solution proposée : Une application de facturation Django, permettant la création de factures, le suivi des statuts et l’export des données.

2. Analyse des Besoins (User Stories)
Acteur,Besoin (User Story)
Dirigeant PME,"""Je veux créer mes factures rapidement et suivre leur statut pour savoir quelles factures sont payées."""

Assistant PME,"""Je veux exporter les factures en CSV pour envoyer les données à mon expert-comptable."""

Collaborateur PME,"""Je veux générer un PDF propre pour chaque facture afin de l’envoyer aux clients."""

3. Spécifications Fonctionnelles (Le périmètre du POC)
Pour le POC, nous nous concentrons sur les fonctionnalités critiques :

Module Facturation : Création, édition et suivi du statut des factures (Brouillon, Envoyée, Payée).

Export : Génération de fichiers CSV et PDF pour les factures.

Dashboard : Consultation des factures récentes, totaux HT, et suivi des factures en attente.

4. Analyse des Risques et Contraintes
Sécurité : Les données financières sont ultra-sensibles. L'architecture doit prévoir un chiffrement et une authentification forte.

Performance : Le système doit répondre en moins de 500ms pour garantir une fluidité d'utilisation.

Intégrité : Une erreur de calcul ou une double saisie est inacceptable en comptabilité (utilisation de PostgreSQL pour la gestion des transactions).

5. Modèle de Données Simplifié (Concepts)
Voici les entités principales qui seront développées :

Entreprise (Nom, SIREN, Coordonnées)

Utilisateur (Nom, Email, Rôle, Entreprise liée)

Facture (Date, Client, Montant HT, TVA, État)

Transaction Bancaire (Date, Libellé, Montant, Statut de rapprochement)