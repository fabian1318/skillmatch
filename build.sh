#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Recolectar archivos estáticos (CSS, JS, Imágenes)
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos de producción
python manage.py migrate

#Crear Superusuario Automáticamente
python create_superuser.py