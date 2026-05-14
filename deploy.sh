#!/bin/bash

# Script de déploiement manuel rapide sur EC2
# Usage: ./deploy.sh <EC2_IP> <SSH_KEY_PATH>

set -e

EC2_IP=${1:-"YOUR_EC2_IP"}
SSH_KEY=${2:-"~/.ssh/facturation-pme-key.pem"}
EC2_USER="ubuntu"

echo "🚀 Déploiement manuel sur $EC2_IP..."

# Copie des fichiers docker
echo "📦 Copie des fichiers Docker..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -r docker ${EC2_USER}@${EC2_IP}:/home/ubuntu/facturation-pme/

# Configuration .env
echo "⚙️  Configuration de l'environnement..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} << 'ENDSSH'
cd /home/ubuntu/facturation-pme

# Créer .env si inexistant
if [ ! -f .env ]; then
    echo "DEBUG=False" > .env
    echo "SECRET_KEY=change-this-to-a-secure-secret-key" >> .env
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0" >> .env
    echo "DB_NAME=facturationpme" >> .env
    echo "DB_USER=facturationpme" >> .env
    echo "DB_PASSWORD=facturationpme" >> .env
    echo "⚠️  IMPORTANT: Modifiez SECRET_KEY et DB_PASSWORD dans .env sur l'instance"
fi
ENDSSH

# Login à GHCR et pull de l'image
echo "🐳 Pull de l'image Docker..."
read -p "Entrez votre GitHub Personal Access Token (pour GHCR): " GITHUB_TOKEN
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "echo $GITHUB_TOKEN | docker login ghcr.io -u frederickmeyapiiii --password-stdin"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "docker pull ghcr.io/frederickmeyapiiii/facturation-pme:latest"

# Redémarrage des conteneurs
echo "🔄 Redémarrage des conteneurs..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "cd /home/ubuntu/facturation-pme/docker && docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up -d"

# Migrations
echo "🗄️  Exécution des migrations..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "cd /home/ubuntu/facturation-pme/docker && docker compose -f docker-compose.prod.yml exec web python manage.py migrate"

echo "✅ Déploiement terminé !"
echo "🌐 Accès: http://$EC2_IP:8000/"
