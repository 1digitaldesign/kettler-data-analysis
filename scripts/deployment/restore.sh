#!/bin/bash
# Restore Script
# Restores data from backups

set -e

BACKUP_FILE=${1:-}
BACKUP_DIR="${BACKUP_DIR:-./backups}"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    echo ""
    echo "Available backups:"
    ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "=== Restoring from Backup ==="
echo "Backup file: $BACKUP_FILE"
echo ""

# Extract backup type from filename
if [[ "$BACKUP_FILE" == *"data_"* ]]; then
    echo "Restoring data directory..."
    tar -xzf "$BACKUP_FILE" -C .
    echo "✓ Data restored"
elif [[ "$BACKUP_FILE" == *"research_"* ]]; then
    echo "Restoring research directory..."
    tar -xzf "$BACKUP_FILE" -C .
    echo "✓ Research restored"
elif [[ "$BACKUP_FILE" == *"vectors_"* ]]; then
    echo "Restoring vector store..."
    tar -xzf "$BACKUP_FILE" -C .
    echo "✓ Vector store restored"
elif [[ "$BACKUP_FILE" == *"config_"* ]]; then
    echo "Restoring configurations..."
    tar -xzf "$BACKUP_FILE" -C .
    echo "✓ Configurations restored"
else
    echo "Unknown backup type. Extracting to current directory..."
    tar -xzf "$BACKUP_FILE" -C .
fi

echo ""
echo "=== Restore Complete ==="
echo "You may need to restart services: docker-compose restart"
