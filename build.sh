#!/bin/bash

# Build the project
set -e  # Exit on error

# Instalar dependencias
pip install -r requirements.txt

pip install --upgrade pip

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

