#!/bin/bash
# Test Hugging Face Authentication
# Verifies that Hugging Face tokens are properly configured

set -e

echo "=== Testing Hugging Face Authentication ==="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "Create .env file with HF_WRITE_TOKEN and HF_READ_TOKEN"
    exit 1
fi

echo "✓ .env file found"
echo ""

# Check Docker Compose config
echo "Checking Docker Compose configuration..."
if docker-compose config | grep -q "HF_WRITE_TOKEN"; then
    echo "✓ HF_WRITE_TOKEN configured in docker-compose"
else
    echo "❌ HF_WRITE_TOKEN not found in docker-compose config"
fi

if docker-compose config | grep -q "HF_READ_TOKEN"; then
    echo "✓ HF_READ_TOKEN configured in docker-compose"
else
    echo "❌ HF_READ_TOKEN not found in docker-compose config"
fi

echo ""

# Test in container
echo "Testing in Python ETL container..."
if docker-compose exec python-etl python scripts/etl/huggingface_auth.py 2>&1 | grep -q "✓"; then
    echo "✓ Authentication test passed"
else
    echo "⚠ Authentication test had issues (check output above)"
fi

echo ""
echo "=== Test Complete ==="
