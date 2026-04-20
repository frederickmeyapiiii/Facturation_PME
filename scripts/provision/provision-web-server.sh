#!/usr/bin/env bash
# ============================================
# provision-web-server.sh
# Configure un serveur Linux Ubuntu pour l'application de facturation PME
# Usage : sudo bash scripts/provision/provision-web-server.sh
# Auteur : Frederic
# Date : 2026-03
# ============================================
set -euo pipefail

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

[[ $EUID -eq 0 ]] || { log "Root requis" >&2; exit 1; }

APP_USER="assistant"
APP_DIR="/opt/facturation_pme"
APP_PORT="8000"
LOG_FILE="/var/log/provision-web-server.log"

exec > >(tee -a "$LOG_FILE") 2>&1

log "Début du provisionnement"

# Mise à jour du système
log "Mise à jour des paquets"
apt-get update -qq
apt-get upgrade -y -qq

# Installation des paquets
log "Installation des paquets nécessaires"
apt-get install -y nginx git ufw python3 python3-venv python3-pip

# Création de l'utilisateur applicatif (idempotent)
if ! id "$APP_USER" &>/dev/null; then
    log "Création de l'utilisateur $APP_USER"
    useradd --system --home-dir "$APP_DIR" --create-home --shell /bin/bash "$APP_USER"
else
    log "Utilisateur $APP_USER existe déjà"
fi

# Configuration Nginx
log "Configuration Nginx"
cat > /etc/nginx/conf.d/facturation_pme.conf <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl enable --now nginx

# Configuration du pare-feu
log "Configuration UFW"
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw --force enable

# Vérification finale
log "Vérification finale"
if systemctl is-active --quiet nginx; then
    log "OK — nginx actif"
else
    log "ERREUR — nginx inactif"
    exit 1
fi

if ufw status | grep -q "Status: active"; then
    log "OK — pare-feu actif"
else
    log "ERREUR — pare-feu inactif"
    exit 1
fi

log "Provisionnement terminé"
