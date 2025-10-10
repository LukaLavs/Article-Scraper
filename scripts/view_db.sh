#!/bin/bash
# ------------------------------
# view_db.sh - Open Postgres DB via Docker on Linux
# ------------------------------

# Exit on error
set -e

# Change to project root (optional, adjust as needed)
cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ".env file not found."
    exit 1
fi

# Export all variables from .env safely
set -a
source .env
set +a


# Connect to the running Postgres container
docker exec -it store-base psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
