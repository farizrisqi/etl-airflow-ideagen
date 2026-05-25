#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

echo "Stopping ETL Airflow IDEAGEN project..."

if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running."
    exit 1
fi

docker-compose down

echo "Project stopped successfully!"
