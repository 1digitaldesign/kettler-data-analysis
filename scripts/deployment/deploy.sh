#!/bin/bash
# Deployment Script
# Handles deployment of services to different environments

set -e

ENVIRONMENT=${1:-development}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "=== Deploying to $ENVIRONMENT ==="
echo ""

case $ENVIRONMENT in
  development)
    echo "Deploying to development..."
    docker-compose up -d --build
    ;;

  staging)
    echo "Deploying to staging..."
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d --build
    ;;

  production)
    echo "Deploying to production..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    ;;

  *)
    echo "Unknown environment: $ENVIRONMENT"
    echo "Usage: $0 [development|staging|production]"
    exit 1
    ;;
esac

echo ""
echo "Waiting for services to start..."
sleep 10

echo ""
echo "Checking service health..."
python3 scripts/monitoring/health_check.py || true

echo ""
echo "=== Deployment Complete ==="
echo "View status: docker-compose ps"
echo "View logs: docker-compose logs -f"
