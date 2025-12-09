#!/bin/bash
# Initialize Microservices
# Ensures all services are properly configured and can communicate

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Initializing Microservices Architecture ==="
echo ""

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose not found"
    exit 1
fi

echo "1. Validating Docker Compose configuration..."
docker-compose config > /dev/null
echo "   ✓ Configuration valid"

echo ""
echo "2. Checking network..."
if docker network ls | grep -q kettler-network; then
    echo "   ✓ Network exists"
else
    echo "   Creating network..."
    docker network create kettler-network
    echo "   ✓ Network created"
fi

echo ""
echo "3. Checking volumes..."
docker-compose config --volumes | while read volume; do
    if docker volume ls | grep -q "$volume"; then
        echo "   ✓ Volume $volume exists"
    else
        echo "   Creating volume $volume..."
        docker volume create "$volume"
    fi
done

echo ""
echo "4. Building images..."
docker-compose build --parallel

echo ""
echo "=== Microservices Initialization Complete ==="
echo ""
echo "Start services with: docker-compose up -d"
