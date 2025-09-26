#!/bin/bash
set -e

echo "Running initialization scripts..."
alembic upgrade head

echo "Starting main application..."
exec "$@"