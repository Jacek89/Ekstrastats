#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
poetry self update

python manage.py collectstatic --no-input
