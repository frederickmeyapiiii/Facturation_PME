#!/bin/bash
set -euo pipefail

# --- Configuration ---
DB_ENGINE="${DB_ENGINE:-postgresql}"
DB_NAME="${DB_NAME:-finance_pro_db}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-../backups}"
DATE=$(date +%Y-%m-%d_%Hh%M)
FILENAME="backup_${DB_NAME}_${DATE}.sql"

# Créer le dossier backup s'il n'existe pas
mkdir -p "$BACKUP_DIR"

echo "🚀 Démarrage de la sauvegarde de $DB_NAME..."

# --- Exécution de la sauvegarde ---
if [ "$DB_ENGINE" = "postgresql" ] || [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
    export PGPASSWORD="$DB_PASSWORD"
    pg_dump -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" "$DB_NAME" > "$BACKUP_DIR/$FILENAME"
elif [ "$DB_ENGINE" = "sqlite3" ] || [ "$DB_ENGINE" = "django.db.backends.sqlite3" ]; then
    cp "$DB_NAME" "$BACKUP_DIR/$FILENAME"
else
    echo "❌ DB_ENGINE '$DB_ENGINE' non supporté"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "✅ Sauvegarde réussie : $BACKUP_DIR/$FILENAME"
else
    echo "❌ Erreur lors de la sauvegarde"
    exit 1
fi

# --- Nettoyage ---
# Supprime les backups de plus de 7 jours pour économiser de l'espace
find $BACKUP_DIR -type f -name "*.sql" -mtime +7 -delete
echo "🧹 Nettoyage des anciennes sauvegardes terminé."