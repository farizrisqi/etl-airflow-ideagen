#!/bin/bash
set -e

echo "📦 Installing requirements.txt..."
pip install --no-cache-dir -r /opt/airflow/requirements.txt

echo "🚀 Starting Airflow..."
exec airflow "$@"
