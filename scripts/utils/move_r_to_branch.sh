#!/bin/bash
# Script to move all R files to r-code-branch

set -e

PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT"

echo "Finding all R and Rmd files..."
R_FILES=$(find . -name "*.R" -o -name "*.Rmd" | grep -v ".git" | grep -v "node_modules")

if [ -z "$R_FILES" ]; then
    echo "No R files found"
    exit 0
fi

echo "Found R files:"
echo "$R_FILES" | head -10
echo "... (and more)"

# Checkout r-code-branch and ensure R files are there
echo ""
echo "Ensuring R files are in r-code-branch..."
git checkout r-code-branch
git checkout main -- $(echo "$R_FILES")

# Commit R files to r-code-branch
git add $(echo "$R_FILES")
git commit -m "Archive all R code files from main branch" || echo "No changes to commit in r-code-branch"

# Switch back to main
git checkout main

# Remove R files from main
echo ""
echo "Removing R files from main branch..."
git rm $(echo "$R_FILES") || echo "Some files may already be removed"

echo ""
echo "R code removal complete. Review changes with 'git status'"
