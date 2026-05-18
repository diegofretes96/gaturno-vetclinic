# ── Stage 1: build de dependencias ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Dependencias del sistema necesarias para psycopg2 y Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ── Stage 2: imagen de producción ───────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# Solo librerías runtime necesarias (sin gcc ni cabeceras)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar paquetes Python instalados desde el stage builder
COPY --from=builder /root/.local /root/.local

# Copiar el código fuente
COPY . .

# Recolectar static files en tiempo de build
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

EXPOSE 8000

# Gunicorn con 2 workers por defecto; ajustar según CPU del servidor
CMD ["gunicorn", "vetclinic.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-"]
