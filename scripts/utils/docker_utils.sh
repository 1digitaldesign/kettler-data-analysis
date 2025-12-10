#!/bin/bash
# Docker Utility Functions
# Common functions for Docker operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project directory
get_project_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
}

# Check if service is running
is_service_running() {
    local service=$1
    docker-compose ps | grep -q "$service.*Up" && return 0 || return 1
}

# Wait for service to be healthy
wait_for_service() {
    local service=$1
    local url=$2
    local max_attempts=30
    local attempt=0

    echo "Waiting for $service to be healthy..."
    while [ $attempt -lt $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $service is healthy"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "  Attempt $attempt/$max_attempts..."
        sleep 2
    done

    echo -e "${RED}✗${NC} $service failed to become healthy"
    return 1
}

# Scale service
scale_service() {
    local service=$1
    local replicas=$2

    echo "Scaling $service to $replicas replicas..."
    docker-compose up -d --scale "$service=$replicas"
    echo -e "${GREEN}✓${NC} Scaled $service to $replicas replicas"
}

# Get service logs
get_service_logs() {
    local service=$1
    local lines=${2:-50}

    echo "=== Logs for $service (last $lines lines) ==="
    docker-compose logs --tail="$lines" "$service"
}

# Restart service
restart_service() {
    local service=$1

    echo "Restarting $service..."
    docker-compose restart "$service"
    echo -e "${GREEN}✓${NC} Restarted $service"
}

# Clean up stopped containers
cleanup_containers() {
    echo "Cleaning up stopped containers..."
    docker-compose down
    docker system prune -f
    echo -e "${GREEN}✓${NC} Cleanup complete"
}

# Show service status
show_status() {
    echo "=== Service Status ==="
    docker-compose ps
    echo ""
    echo "=== Resource Usage ==="
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}
