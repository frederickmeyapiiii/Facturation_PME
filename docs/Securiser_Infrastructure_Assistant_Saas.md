# Sécuriser l’infrastructure – Assistant Saas

## 1. Objectif

Ce document présente la sécurisation de l’infrastructure du projet **Assistant Saas**.
Il explique les mesures prises pour l’accès SSH, le pare-feu, les mises à jour et les pratiques de durcissement.

Ce document fait partie du dossier de projet et est destiné à être lu par le jury.

## 2. Contexte

Le projet Assistant Saas est une application Django de gestion de factures et de sociétés.
Même si le projet est développé localement, la sécurisation est conçue comme une pratique intégrée : la sécurité doit être appliquée par défaut, pas activée seulement si on le demande.

## 3. Principes de sécurité appliqués

### 3.1 Principe du moindre privilège

- Seuls les services nécessaires sont activés.
- Chaque port ouvert est justifié.
- Les règles de pare-feu sont restrictives par défaut.

### 3.2 Hardening système

Mesures attendues :
- Mise à jour régulière du système et des paquets.
- Suppression des paquets inutiles.
- Vérification des services actifs.
- Fermeture des ports non nécessaires.

### 3.3 Application des recommandations ANSSI

Le dossier fait référence aux guides de l’ANSSI pour :
- l’administration sécurisée d’un système GNU/Linux,
- la gestion des accès SSH,
- la configuration du pare-feu.

## 4. Authentification SSH sécurisée

### 4.1 Clé SSH Ed25519

- Utilisation d’une clé Ed25519 pour l’accès SSH.
- La clé privée reste sur le poste client.
- La clé publique est installée dans `~/.ssh/authorized_keys` sur le serveur.

### 4.2 Configuration SSH

Paramètres recommandés dans `/etc/ssh/sshd_config` :
- `PermitRootLogin no`
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`
- `AuthorizedKeysFile .ssh/authorized_keys`
- `X11Forwarding no`
- `AllowAgentForwarding no`
- `MaxAuthTries 3`
- `LoginGraceTime 30`

### 4.3 Prévention du verrouillage

- Toujours tester la nouvelle configuration SSH depuis une seconde session avant de fermer la connexion existante.

### 4.4 Protection contre le brute force

- Installation et configuration de `fail2ban`.
- Règles suggérées :
  - `maxretry = 5`
  - `findtime = 600`
  - `bantime = 3600`

## 5. Pare-feu système

### 5.1 Politique UFW

La politique du pare-feu local est :
- `ufw default deny incoming`
- `ufw default allow outgoing`
- `ufw default deny forward`

### 5.2 Règles ouvertes

Exemples de règles :
- `ufw allow 22/tcp` pour SSH (ou le port personnalisé si utilisé)
- `ufw allow 443/tcp` pour HTTPS
- `ufw allow 80/tcp` si HTTP est utilisé uniquement pour redirection vers HTTPS

### 5.2.1 Tableau de règles UFW

| Port / Service | Protocole | Source | Justification |
|---|---|---|---|
| 22 / SSH | TCP | 10.0.0.0/8 ou VPN interne | Accès sécurisé du personnel d’exploitation. SSH doit être limité pour réduire la surface d’attaque. |
| 443 / HTTPS | TCP | 0.0.0.0/0 | Permet l’accès public sécurisé à l’application web. |
| 80 / HTTP | TCP | 0.0.0.0/0 | Redirection vers HTTPS uniquement. Pas d’accès direct à l’application en clair. |
| 5432 / PostgreSQL (ou base interne) | TCP | 192.168.1.0/24 | Accès uniquement depuis le serveur applicatif interne. La base de données n’est pas exposée sur Internet. |
| 8080 / Monitoring (optionnel) | TCP | 127.0.0.1 ou réseau interne | Interface de supervision accessible uniquement localement ou depuis le réseau de gestion.

### 5.3 Restriction par source

Quand c’est possible, limiter l’accès par source IP :
- SSH uniquement depuis le réseau de confiance
- Base de données uniquement depuis le serveur applicatif

### 5.4 Vérification

- `ufw status verbose`
- justification de chaque règle dans le dossier de projet

## 6. Certificats TLS

### 6.1 Objectif

- Chiffrer les échanges entre les utilisateurs et l’application.
- Éviter l’exposition des données en clair sur le réseau.

### 6.2 Mise en œuvre

- Pour un service exposé sur Internet : Let’s Encrypt via Certbot.
- Pour un environnement privé ou local : PKI interne avec certificats signés par une CA locale.

### 6.3 Configuration recommandée

- `ssl_protocols TLSv1.2 TLSv1.3;`
- Désactiver TLS 1.0 et TLS 1.1.
- HSTS activé sur 1 an si le service est public.

## 7. Environnements de test et mises à jour

### 7.1 Environnement de test

- Le projet doit pouvoir être vérifié sur un serveur de test ou une VM isolée avant production.
- Le test valide les mises à jour, la configuration du pare-feu et le fonctionnement SSH/TLS.

### 7.2 Processus de mise à jour

- Mise à jour sur l’environnement de staging
- Vérification post-mise à jour par un test de santé (`health check`)
- Passage en production uniquement après validation

### 7.3 Politique de mise à jour

Le dossier doit documenter :
- fréquence des mises à jour,
- distinction mises à jour de sécurité / mises à jour fonctionnelles,
- processus de validation et de rollback.

### 7.4 Automatisation des mises à jour

- Utilisation possible de `unattended-upgrades` pour les correctifs de sécurité.
- Simulation de mise à jour avec `unattended-upgrade --dry-run --debug`.

## 8. Preuves à inclure dans le dossier

- Extrait commenté de `/etc/ssh/sshd_config`.
- Capture de `ufw status verbose` avec justification des règles.
- Sortie de `fail2ban-client status sshd`.
- Preuve de configuration TLS (certificat, tests openssl, score SSL Labs si possible).
- Description du processus de mise à jour et de test avant déploiement.

## 9. Correspondance avec CP3

Ce dossier montre que :
- les accès SSH sont sécurisés,
- le pare-feu local est en place,
- les certificats TLS sont prévus,
- les mises à jour sont testées avant production,
- la documentation de sécurité est rédigée.

## 10. Où mettre ce document ?

- Dans `docs/` avec le CDC et les autres documents de projet.
- Le jury peut lire ce document comme la partie sécurité de ton dossier professionnel.

## 11. Conseils pour l’oral

- Explique que la sécurité a été appliquée sans demande explicite du client.
- Donne un exemple concret : SSH par clés, UFW par défaut deny, TLS et tests de mise à jour.
- Conclue sur le fait que tu pratiques la sécurité comme un réflexe, pas comme une option.
