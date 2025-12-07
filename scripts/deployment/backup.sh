#!/bin/bash
# Backup Script
# Backs up data volumes and configurations

set -e

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

mkdir -p "$BACKUP_DIR"

echo "=== Creating Backup ==="
echo "Timestamp: $TIMESTAMP"
echo "Backup directory: $BACKUP_DIR"
echo ""

# Backup data directory
if [ -d "data" ]; then
    echo "Backing up data directory..."
    tar -czf "$BACKUP_DIR/data_$TIMESTAMP.tar.gz" data/
    echo "✓ Data backup created"
fi

# Backup research directory
if [ -d "research" ]; then
    echo "Backing up research directory..."
    tar -czf "$BACKUP_DIR/research_$TIMESTAMP.tar.gz" research/
    echo "✓ Research backup created"
fi

# Backup vector store
if [ -d "data/vectors" ]; then
    echo "Backing up vector store..."
    tar -czf "$BACKUP_DIR/vectors_$TIMESTAMP.tar.gz" data/vectors/
    echo "✓ Vector store backup created"
fi

# Backup configurations
echo "Backing up configurations..."
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    docker-compose.yml \
    kubernetes/ \
    docker/ \
    2>/dev/null || true
echo "✓ Configuration backup created"

echo ""
echo "=== Backup Complete ==="
echo "Backup location: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"/*_$TIMESTAMP.tar.gz
