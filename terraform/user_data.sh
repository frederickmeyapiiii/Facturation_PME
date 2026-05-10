#!/bin/bash

# Script d'initialisation rapide pour l'instance EC2
# Ce script installe Docker et prépare l'environnement pour un déploiement rapide

set -e

echo "🚀 Début de l'initialisation de l'instance..."

# Mise à jour rapide du système
echo "📦 Mise à jour du système..."
sudo apt update -y

# Installation de Docker
echo "🐳 Installation de Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Installation de Docker Compose
echo "🔧 Installation de Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Installation de Git
echo "📚 Installation de Git..."
sudo apt install -y git

# Configuration du pare-feu
echo "🔒 Configuration du pare-feu..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Création du répertoire pour l'application
echo "📁 Création du répertoire de l'application..."
mkdir -p /home/ubuntu/facturation-pme
chown ubuntu:ubuntu /home/ubuntu/facturation-pme

echo "✅ Initialisation terminée !"

# Configuration de Nginx comme reverse proxy
cat > /etc/nginx/sites-available/facturation-pme << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/facturation-pme /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl enable nginx
systemctl start nginx

echo "✅ Initialisation EC2 terminée"
