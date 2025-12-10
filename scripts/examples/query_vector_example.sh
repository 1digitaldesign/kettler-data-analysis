#!/bin/bash
# Example: Query Vector Embeddings
# Demonstrates how to query the vector embedding API

set -e

API_URL="http://localhost:8000"

echo "=== Vector Embedding Query Examples ==="
echo ""

# Health check
echo "1. Health Check:"
curl -s "$API_URL/health" | python3 -m json.tool
echo ""

# Get statistics
echo "2. Vector Store Statistics:"
curl -s "$API_URL/api/v1/stats" | python3 -m json.tool
echo ""

# Search for similar content
echo "3. Search Similar Content:"
QUERY="${1:-Caitlin Skidmore}"
echo "Query: $QUERY"
curl -s -X POST "$API_URL/api/v1/search" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY\", \"top_k\": 10}" | python3 -m json.tool
echo ""

# Create embedding
echo "4. Create Embedding:"
TEXT="${2:-Sample text for embedding}"
echo "Text: $TEXT"
curl -s -X POST "$API_URL/api/v1/embed" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$TEXT\", \"source\": \"example\"}" | python3 -m json.tool
echo ""

echo "=== Examples Complete ==="
