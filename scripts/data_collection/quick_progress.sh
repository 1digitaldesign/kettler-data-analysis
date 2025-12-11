#!/bin/bash
# Quick Progress Bar Display
# Simple one-liner to show current progress

cd "$(dirname "$0")/../.."
python3 scripts/data_collection/live_progress_bar.py
