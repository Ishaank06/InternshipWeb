#!/bin/bash
# Startup script for Academia - Industry Collaboration Portal

echo "=========================================================="
echo " Starting Academia-Industry Collaboration Portal (Topic 55)"
echo "=========================================================="

# Run migrations if needed
python3 manage.py migrate

# Start development server on port 8080
echo "Starting server on http://127.0.0.1:8080"
python3 manage.py runserver 0.0.0.0:8080
