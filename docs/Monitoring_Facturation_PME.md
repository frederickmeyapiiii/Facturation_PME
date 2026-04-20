# Monitoring — Facturation PME

## Vue d'ensemble

Ce projet intègre un système de monitoring basé sur **Prometheus** pour la collecte des métriques et **Grafana** pour la visualisation.
Les services Django et PostgreSQL exposent leurs métriques, permettant un suivi en temps réel de l'état du système.

## Composants

- **Prometheus** : collecteur de métriques (port 9090)
- **Grafana** : tableau de bord de visualisation (port 3000)
- **PostgreSQL** : base de données avec exporter
- **Django** : application exposant des métriques

## Fichiers de configuration

- `docker-compose.monitoring.yml` : stack de monitoring
- `monitoring/prometheus.yml` : configuration des targets Prometheus
- `monitoring/grafana/provisioning/` : configuration auto de Grafana

## Démarrage du monitoring

### Option 1 : Avec le compose de monitoring

```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

Cela lance :
- Django sur le port 8000
- PostgreSQL
- Prometheus sur le port 9090
- Grafana sur le port 3000

### Option 2 : Monitoring seul (test)

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

## Accès aux dashboards

- **Prometheus** : http://localhost:9090
- **Grafana** : http://localhost:3000 (admin / admin par défaut)

## Configuration Grafana

1. Accéder à http://localhost:3000
2. Se connecter avec `admin` / `admin`
3. Ajouter une datasource Prometheus : http://prometheus:9090
4. Créer des dashboards pour visualiser :
   - Nombre de requêtes
   - Temps de réponse
   - Erreurs HTTP
   - Utilisation CPU/RAM
   - Connexions à PostgreSQL

## Métriques collectées

### Django
- Requêtes HTTP (nombre, latence)
- Erreurs (4xx, 5xx)
- Temps de traitement

### PostgreSQL
- Connexions actives
- Requêtes exécutées
- Utilisation du disque

## Extensions futures

- Exporter de métriques personnalisées (nombre de factures créées, etc.)
- Alertes Prometheus (ex: erreur 5xx > 5% sur 5 min)
- Intégration avec Alertmanager pour les notifications

## Notes

- Les données Prometheus sont conservées dans un volume Docker
- Grafana stocke ses configurations et dashboards
- Les mots de passe par défaut doivent être changés en production
