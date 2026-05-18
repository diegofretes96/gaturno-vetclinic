#!/bin/bash
echo "=== VetClinic – Setup ==="
pip install -r requirements.txt
cp .env.example .env
echo ""
echo "Edita .env con tus credenciales de base de datos, luego ejecuta:"
echo "  python manage.py migrate"
echo "  python manage.py runserver"
echo ""
echo "Para cargar datos iniciales (especies, razas, vacunas, etc.):"
echo "  python manage.py shell < fixtures/seed_data.py"
