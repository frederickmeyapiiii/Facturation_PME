# Déploiement AWS avec Terraform

Ce guide explique comment déployer l'application Facturation PME sur AWS en utilisant Terraform.

## Prérequis

- Compte AWS actif
- Terraform installé (v1.0+)
- AWS CLI configuré avec vos credentials
- Clé SSH AWS créée

## Configuration des credentials AWS

### Option 1: AWS CLI

```bash
aws configure
```

Entrez vos credentials AWS (Access Key ID, Secret Access Key, Region: eu-west-3).

### Option 2: Variables d'environnement

```bash
export AWS_ACCESS_KEY_ID="votre_access_key"
export AWS_SECRET_ACCESS_KEY="votre_secret_key"
export AWS_DEFAULT_REGION="eu-west-3"
```

### Option 3: Fichier credentials

Créez le fichier `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = VOTRE_ACCESS_KEY
aws_secret_access_key = VOTRE_SECRET_KEY
```

Et le fichier `~/.aws/config`:

```ini
[default]
region = eu-west-3
```

## Création de la clé SSH AWS

1. Allez dans la console AWS EC2 > Key Pairs
2. Cliquez sur "Create Key Pair"
3. Nommez-la `facturation-pme-key`
4. Téléchargez le fichier `.pem`
5. Déplacez-le dans le dossier terraform:

```bash
mv ~/Downloads/facturation-pme-key.pem terraform/
chmod 400 terraform/facturation-pme-key.pem
```

## Configuration Terraform

1. Copiez le fichier d'exemple:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

2. Éditez `terraform/terraform.tfvars` avec vos valeurs:

```hcl
aws_region     = "eu-west-3"
environment    = "dev"
project_name   = "facturation-pme"
ssh_key_name   = "facturation-pme-key"
db_username    = "facturationpme"
db_password    = "votre_mot_de_passe_securise"
domain_name    = "facturation-pme.com"
```

## Déploiement

### 1. Initialisation Terraform

```bash
cd terraform
terraform init
```

### 2. Validation de la configuration

```bash
terraform validate
terraform plan
```

### 3. Application de l'infrastructure

```bash
terraform apply
```

Confirmez avec `yes` quand demandé.

### 4. Récupération de l'IP publique

```bash
terraform output web_instance_public_ip
```

## Déploiement de l'application

Une fois l'instance créée, déployez l'application:

```bash
# Rendez le script exécutable
chmod +x terraform/deploy.sh

# Déployez avec l'IP publique et la clé SSH
./terraform/deploy.sh <IP_PUBLIQUE> terraform/facturation-pme-key.pem
```

## Accès à l'application

- **Application**: http://<IP_PUBLIQUE>
- **SSH**: `ssh -i terraform/facturation-pme-key.pem ubuntu@<IP_PUBLIQUE>`

## Gestion

### Voir les logs

```bash
ssh -i terraform/facturation-pme-key.pem ubuntu@<IP_PUBLIQUE> \
  'sudo docker-compose -f /home/ubuntu/facturation-pme/docker/docker-compose.yml logs -f'
```

### Redémarrer l'application

```bash
ssh -i terraform/facturation-pme-key.pem ubuntu@<IP_PUBLIQUE> \
  'cd /home/ubuntu/facturation-pme && sudo docker-compose -f docker/docker-compose.yml restart'
```

### Mettre à jour l'application

```bash
# Copiez les nouveaux fichiers
scp -i terraform/facturation-pme-key.pem -r src ubuntu@<IP_PUBLIQUE>:/home/ubuntu/facturation-pme/
scp -i terraform/facturation-pme-key.pem -r docker ubuntu@<IP_PUBLIQUE>:/home/ubuntu/facturation-pme/

# Rebuild et redémarrez
ssh -i terraform/facturation-pme-key.pem ubuntu@<IP_PUBLIQUE> \
  'cd /home/ubuntu/facturation-pme && sudo docker-compose -f docker/docker-compose.yml up -d --build'
```

## Destruction

Pour détruire toute l'infrastructure:

```bash
cd terraform
terraform destroy
```

## Coûts estimés (eu-west-3)

- **Instance EC2 t3.micro**: ~€8-12/mois
- **RDS db.t3.micro**: ~€15-20/mois
- **Autres ressources**: ~€5-10/mois
- **Total dev**: ~€30-40/mois

## Sécurité

- Changez le mot de passe par défaut dans `terraform.tfvars`
- Restreignez l'accès SSH à votre IP en production
- Utilisez des secrets AWS pour les mots de passe
- Activez le backend S3 pour le state Terraform après le premier déploiement

## Support

En cas de problème:

1. Vérifiez les logs Terraform: `terraform show`
2. Consultez les logs EC2 dans la console AWS
3. Vérifiez les security groups
4. Testez la connexion SSH
