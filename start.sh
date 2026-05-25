#!/bin/bash

cd "$(dirname "$0")"

echo "Starting ETL Airflow IDEAGEN project..."

if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

echo "Stopping any existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true

# Step 1: Start DB only first
echo "Starting database..."
if ! docker-compose up -d airflow-postgres; then
    echo "Error: Failed to start database."
    exit 1
fi

# Step 2: Wait for postgres to actually be ready
echo "Waiting for airflow-postgres to be ready..."
MAX_WAIT=60
WAITED=0
until docker-compose exec -T airflow-postgres pg_isready -U airflow > /dev/null 2>&1; do
    if [ "$WAITED" -ge "$MAX_WAIT" ]; then
        echo "Error: Database not ready after ${MAX_WAIT}s, aborting."
        exit 1
    fi
    echo "  Waiting for database... (${WAITED}s elapsed)"
    sleep 5
    WAITED=$((WAITED + 5))
done
echo "Database is ready."

# Step 3: Initialize Airflow DB via one-off container (before webserver starts)
# Note: entrypoint.sh already prepends "airflow", so pass subcommand only (e.g. "db init" not "airflow db init")
echo "Initializing Airflow database..."
docker-compose run --rm airflow-webserver db init
echo "Database initialized."

# Step 4: Create admin user
echo "Creating admin user..."
docker-compose run --rm airflow-webserver users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com 2>&1 | grep -v "already exist" || true

# Step 5: Start all remaining services (webserver & scheduler now safe to start)
echo "Starting all services..."
if ! docker-compose up -d --remove-orphans; then
    echo "Error: Failed to start Docker services."
    exit 1
fi

echo ""
echo "Service status:"
docker-compose ps

echo ""
echo "Project started successfully!"
echo "  Airflow webserver : http://localhost:8080"
echo "  PostgreSQL (CDC)  : localhost:5432"
