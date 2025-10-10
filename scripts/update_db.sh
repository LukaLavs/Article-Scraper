#!/bin/bash
# ------------------------------
# update_db.sh - Run Python script with PYTHONPATH set
# ------------------------------

# Exit on error
set -e

# Change to project root (parent directory of the script)
cd "$(dirname "$0")/.."

# Set PYTHONPATH to the src folder
export PYTHONPATH="$PWD/src"

# Run the Python script
python3 src/scripts/update_db.py
