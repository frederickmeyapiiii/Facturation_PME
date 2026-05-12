# Diagramme d'infrastructure AWS — Facturation PME

## Architecture de déploiement sur AWS

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "VPC eu-west-3"
            subgraph "Public Subnet"
                EC2[EC2 Instance<br/>13.36.243.107<br/>Ubuntu 22.04 LTS]
                SG[Security Group<br/>Port 22 (SSH)<br/>Port 8000 (HTTP)<br/>Port 443 (HTTPS)]
            end
            
            subgraph "Internet Gateway"
                IGW[Internet Gateway]
            end
        end
    end
    
    subgraph "EC2 Instance"
        subgraph "Docker Containers"
            Django[Django App<br/>Port 8000]
            Postgres[PostgreSQL<br/>Port 5432]
        end
        
        subgraph "Application Layer"
            App[Facturation PME<br/>Django Application]
            DB[(PostgreSQL<br/>Database)]
        end
    end
    
    subgraph "External"
        User[Utilisateur]
        GitHub[GitHub Actions<br/>CI/CD Pipeline]
        Dev[Developer<br/>Local Machine]
    end
    
    %% Connections
    User -->|HTTPS| IGW
    IGW --> SG
    SG --> EC2
    EC2 --> Django
    Django --> Postgres
    
    GitHub -->|SSH Deploy| EC2
    Dev -->|SSH Admin| EC2
    
    %% Internal connections
    Django --> App
    Postgres --> DB
    
    %% Styling
    classDef aws fill:#e6f3ff,stroke:#0066cc,stroke-width:2px
    classDef ec2 fill:#d4edda,stroke:#28a745,stroke-width:2px
    classDef docker fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    classDef external fill:#f8d7da,stroke:#dc3545,stroke-width:2px
    
    class IGW,SG aws
    class EC2 ec2
    class Django,Postgres docker
    class User,GitHub,Dev external
```

## Flux de déploiement

1. **Développeur** push le code sur GitHub
2. **GitHub Actions** se déclenche automatiquement :
   - Tests unitaires Django
   - Build image Docker
   - Scan de sécurité Trivy
   - Déploiement via SSH sur EC2
3. **EC2 Instance** reçoit le déploiement :
   - Pull de l'image Docker depuis GitHub Container Registry
   - Redémarrage des conteneurs avec docker-compose.prod.yml
   - Exécution des migrations Django

## Flux utilisateur

1. **Utilisateur** accède à l'application via HTTP/HTTPS
2. **Load Balancer** (optionnel) distribue le trafic
3. **Django App** traite les requêtes
4. **PostgreSQL** stocke les données

## Sécurité

- **Security Group** : Ports 22 (SSH), 8000 (HTTP), 443 (HTTPS)
- **SSH CIDR** : Restreint via variable Terraform (`var.ssh_cidr`)
- **Pare-feu UFW** : Configuré sur l'instance EC2
- **HTTPS** : Configuré pour le port 443 (certificat SSL à ajouter)

## Monitoring

**CloudWatch (recommandé pour la production)** :
- Monitoring natif AWS intégré
- Métriques EC2 : CPU, mémoire, disque, réseau
- Alertes configurables avec SNS
- Logs centralisés via CloudWatch Logs
- Coûts prévisibles et aucune maintenance

**Prometheus/Grafana** :
- Optionnel pour monitoring avancé
- Nécessite une instance dédiée ou conteneur
- Plus complexe à maintenir en production

## Scalabilité

- **Horizontal** : Ajout d'instances EC2 via Auto Scaling Group
- **Vertical** : Upgrade de la taille d'instance EC2
- **Base de données** : Migration vers RDS pour la haute disponibilité
