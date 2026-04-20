#!/usr/bin/env bash
# ============================================
# check-web-server.sh
# Vérifie le bon fonctionnement du serveur web de facturation PME
# Usage : sudo bash scripts/provision/check-web-server.sh
# Auteur : Frederic
# Date : 2026-03
# ============================================
set -euo pipefail

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

[[ $EUID -eq 0 ]] || { log "Root requis" >&2; exit 1; }

log "Vérification de l'état de Nginx"
if systemctl is-active --quiet nginx; then
    log "OK — nginx actif"
else
    echo "ERREUR — nginx inactif" >&2
    exit 1
fi

log "Vérification de l'état du pare-feu UFW"
if ufw status | grep -q "Status: active"; then
    log "OK — UFW actif"
else
    echo "ERREUR — UFW inactif" >&2
    exit 1
fi

log "Vérification du port HTTP"
if ss -tlnp | grep -q ':80 '; then
    log "OK — port 80 en écoute"
else
    echo "ERREUR — port 80 non trouvé" >&2
    exit 1
fi

log "Vérification de l'accès local"
if curl -fs http://127.0.0.1/ >/dev/null; then
    log "OK — accès local HTTP fonctionnel"
else
    echo "ERREUR — accès local HTTP impossible" >&2
    exit 1
fi

log "Vérification terminée — serveur opérationnel"
