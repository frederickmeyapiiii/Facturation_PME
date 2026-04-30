#!/bin/bash

# Script de configuration des permissions pour l'application Facturation PME
# Ce script configure les permissions appropriées pour les fichiers et répertoires
# de l'application Django en environnement de développement/production local

set -e

echo "=== Configuration des permissions pour Facturation PME ==="

# Variables
APP_USER="${APP_USER:-www-data}"
APP_GROUP="${APP_GROUP:-www-data}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SRC_DIR="${PROJECT_ROOT}/src"
MEDIA_DIR="${SRC_DIR}/media"
STATIC_DIR="${SRC_DIR}/static"
LOG_DIR="${SRC_DIR}/logs"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si le script est exécuté avec sudo
if [ "$EUID" -ne 0 ]; then
    log_warn "Ce script doit être exécuté avec sudo ou en tant que root"
    log_warn "Exécution avec sudo..."
    exec sudo "$0" "$@"
fi

# Créer les répertoires nécessaires s'ils n'existent pas
log_info "Création des répertoires nécessaires..."
mkdir -p "${MEDIA_DIR}"
mkdir -p "${STATIC_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p "${SRC_DIR}/.venv"

# Définir les permissions pour les répertoires
log_info "Configuration des permissions des répertoires..."

# Permissions pour le répertoire media (écriture par l'application)
chmod 755 "${MEDIA_DIR}"
chown -R "${APP_USER}:${APP_GROUP}" "${MEDIA_DIR}"

# Permissions pour le répertoire static (lecture par le serveur web)
chmod 755 "${STATIC_DIR}"
chown -R "${APP_USER}:${APP_GROUP}" "${STATIC_DIR}"

# Permissions pour le répertoire logs (écriture par l'application)
chmod 755 "${LOG_DIR}"
chown -R "${APP_USER}:${APP_GROUP}" "${LOG_DIR}"

# Permissions pour l'environnement virtuel
chmod 755 "${SRC_DIR}/.venv"
chown -R "${APP_USER}:${APP_GROUP}" "${SRC_DIR}/.venv"

# Permissions pour les fichiers Python
log_info "Configuration des permissions des fichiers Python..."
find "${SRC_DIR}" -type f -name "*.py" -exec chmod 644 {} \;
chown -R "${APP_USER}:${APP_GROUP}" "${SRC_DIR}"

# Permissions pour les fichiers de configuration
log_info "Configuration des permissions des fichiers de configuration..."
if [ -f "${SRC_DIR}/.env" ]; then
    chmod 600 "${SRC_DIR}/.env"
    chown "${APP_USER}:${APP_GROUP}" "${SRC_DIR}/.env"
    log_info "Permissions appliquées sur .env (600)"
fi

# Permissions pour les fichiers de base de données SQLite (si utilisés)
if [ -f "${SRC_DIR}/db.sqlite3" ]; then
    chmod 640 "${SRC_DIR}/db.sqlite3"
    chown "${APP_USER}:${APP_GROUP}" "${SRC_DIR}/db.sqlite3"
    log_info "Permissions appliquées sur db.sqlite3 (640)"
fi

# Permissions pour les fichiers de migration
log_info "Configuration des permissions des fichiers de migration..."
find "${SRC_DIR}" -type d -name "migrations" -exec chmod 755 {} \;

# Permissions pour les templates
log_info "Configuration des permissions des templates..."
find "${SRC_DIR}" -type d -name "templates" -exec chmod 755 {} \;
find "${SRC_DIR}" -type f -name "*.html" -exec chmod 644 {} \;

# Permissions pour les fichiers statiques collectés
if [ -d "${STATIC_DIR}/css" ]; then
    chmod -R 755 "${STATIC_DIR}/css"
    chown -R "${APP_USER}:${APP_GROUP}" "${STATIC_DIR}/css"
fi

if [ -d "${STATIC_DIR}/js" ]; then
    chmod -R 755 "${STATIC_DIR}/js"
    chown -R "${APP_USER}:${APP_GROUP}" "${STATIC_DIR}/js"
fi

if [ -d "${STATIC_DIR}/img" ]; then
    chmod -R 755 "${STATIC_DIR}/img"
    chown -R "${APP_USER}:${APP_GROUP}" "${STATIC_DIR}/img"
fi

# Permissions pour les fichiers uploadés dans media
log_info "Configuration des permissions des fichiers uploadés..."
find "${MEDIA_DIR}" -type f -exec chmod 644 {} \;
find "${MEDIA_DIR}" -type d -exec chmod 755 {} \;

# Permissions pour les fichiers de logs
log_info "Configuration des permissions des fichiers de logs..."
if [ -f "${LOG_DIR}/django.log" ]; then
    chmod 640 "${LOG_DIR}/django.log"
    chown "${APP_USER}:${APP_GROUP}" "${LOG_DIR}/django.log"
fi

if [ -f "${LOG_DIR}/gunicorn.log" ]; then
    chmod 640 "${LOG_DIR}/gunicorn.log"
    chown "${APP_USER}:${APP_GROUP}" "${LOG_DIR}/gunicorn.log"
fi

# Permissions pour le script manage.py
if [ -f "${SRC_DIR}/manage.py" ]; then
    chmod 755 "${SRC_DIR}/manage.py"
    chown "${APP_USER}:${APP_GROUP}" "${SRC_DIR}/manage.py"
    log_info "Permissions appliquées sur manage.py (755)"
fi

# Permissions pour les scripts de provisionnement
log_info "Configuration des permissions des scripts de provisionnement..."
find "${PROJECT_ROOT}/scripts" -type f -name "*.sh" -exec chmod 755 {} \;

# Vérifier les permissions appliquées
log_info "Vérification des permissions appliquées..."
echo ""
echo "Répertoires principaux:"
ls -ld "${MEDIA_DIR}" "${STATIC_DIR}" "${LOG_DIR}" "${SRC_DIR}/.venv" 2>/dev/null || true

echo ""
echo "Fichiers de configuration:"
ls -l "${SRC_DIR}/.env" "${SRC_DIR}/db.sqlite3" 2>/dev/null || true

echo ""
log_info "Configuration des permissions terminée avec succès!"
log_info "Les fichiers et répertoires sont maintenant configurés pour l'utilisateur ${APP_USER}:${APP_GROUP}"

# Instructions pour Docker
if [ -d "${PROJECT_ROOT}/docker" ]; then
    log_warn "Note: Si vous utilisez Docker, les permissions sont gérées par les volumes Docker"
    log_warn "Ce script est principalement pour les déploiements hors Docker"
fi

exit 0
