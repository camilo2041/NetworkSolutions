#!/bin/bash

# Build the project
set -e  # Exit on error

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Eliminar archivos estáticos antiguos
rm -rf /opt/render/project/src/static

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones a la base de datos
python manage.py migrate
