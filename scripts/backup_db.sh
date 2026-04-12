#!/bin/bash

# --- Configuration ---
DB_NAME="finance_pro_db"
BACKUP_DIR="../backups"
DATE=$(date +%Y-%m-%d_%Hh%M)
FILENAME="backup_${DB_NAME}_${DATE}.sql"

# Créer le dossier backup s'il n'existe pas
mkdir -p $BACKUP_DIR

echo "🚀 Démarrage de la sauvegarde de $DB_NAME..."

# --- Exécution de la sauvegarde ---
# pg_dump est l'outil standard de PostgreSQL pour l'export
pg_dump $DB_NAME > $BACKUP_DIR/$FILENAME

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