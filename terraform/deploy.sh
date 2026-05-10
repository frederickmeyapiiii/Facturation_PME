#!/bin/bash

# Script de déploiement pour l'application Django sur EC2
# Usage: ./deploy.sh <IP_PUBLIQUE> <CHEMIN_CLE_SSH>

set -e

IP_PUBLIQUE=$1
SSH_KEY=$2

if [ -z "$IP_PUBLIQUE" ] || [ -z "$SSH_KEY" ]; then
    echo "Usage: $0 <IP_PUBLIQUE> <CHEMIN_CLE_SSH>"
    exit 1
fi

echo "🚀 Déploiement de l'application sur $IP_PUBLIQUE..."

# Attendre que l'instance soit prête
echo "⏳ Attente de la disponibilité de l'instance..."
while ! ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@$IP_PUBLIQUE "echo 'Instance prête'" 2>/dev/null; do
    echo "🔄 En attente de l'instance..."
    sleep 5
done

echo "✅ Instance accessible !"

# Installation des dépendances
echo "📦 Installation des dépendances..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ubuntu@$IP_PUBLIQUE << 'EOF'
    # Mise à jour du système
    sudo apt update && sudo apt upgrade -y
    
    # Installation de Docker et Docker Compose
    if ! command -v docker &> /dev/null; then
        echo "Installation de Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker ubuntu
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "Installation de Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Installation de git et autres outils
    sudo apt install -y git htop
    
    # Création du répertoire de l'application
    mkdir -p /home/ubuntu/facturation-pme
    cd /home/ubuntu/facturation-pme
EOF

# Copie des fichiers du projet
echo "📋 Copie des fichiers du projet..."
scp -i "$SSH_KEY" -r -o StrictHostKeyChecking=no ../src ubuntu@$IP_PUBLIQUE:/home/ubuntu/facturation-pme/
scp -i "$SSH_KEY" -r -o StrictHostKeyChecking=no ../docker ubuntu@$IP_PUBLIQUE:/home/ubuntu/facturation-pme/
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no ../requirements.txt ubuntu@$IP_PUBLIQUE:/home/ubuntu/facturation-pme/

# Configuration et démarrage
echo "🔧 Configuration et démarrage de l'application..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ubuntu@$IP_PUBLIQUE << 'EOF'
    cd /home/ubuntu/facturation-pme
    
    # Création du fichier .env pour la production
    cat > .env << ENVEOF
        DEBUG=False
        SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
        ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
        DATABASE_URL=postgresql://facturationpme:your_password_here@localhost:5432/facturationpme
    ENVEOF
    
    # Construction et démarrage des conteneurs
    sudo docker-compose -f docker/docker-compose.yml down
    sudo docker-compose -f docker/docker-compose.yml up -d --build
    
    # Attendre que les conteneurs soient prêts
    echo "⏳ Attente des conteneurs..."
    sleep 30
    
    # Vérification du statut
    sudo docker-compose -f docker/docker-compose.yml ps
    
    # Migration de la base de données
    sudo docker-compose -f docker/docker-compose.yml exec web python manage.py migrate
    
    # Création d'un superutilisateur (à faire manuellement)
    echo "👤 Pour créer un superutilisateur, exécutez :"
    echo "   sudo docker-compose -f docker/docker-compose.yml exec web python manage.py createsuperuser"
EOF

echo "✅ Déploiement terminé !"
echo "🌐 Application accessible sur: http://$IP_PUBLIQUE:8000"
echo "🔑 Pour vous connecter: ssh -i $SSH_KEY ubuntu@$IP_PUBLIQUE"
echo "📊 Pour voir les logs: ssh -i $SSH_KEY ubuntu@$IP_PUBLIQUE 'sudo docker-compose -f /home/ubuntu/facturation-pme/docker/docker-compose.yml logs -f'"
