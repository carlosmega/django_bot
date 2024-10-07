#!/bin/bash
# Instalar Xvfb
apt-get update && apt-get install -y xvfb

# Configurar y lanzar Xvfb
Xvfb :99 -screen 0 1024x768x24 &

# Exportar el entorno DISPLAY
export DISPLAY=:99

# Iniciar la aplicación Django
python manage.py runserver 0.0.0.0:8000
