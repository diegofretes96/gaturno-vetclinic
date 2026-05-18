#!/usr/bin/env bash
# =============================================================================
#  deploy.sh — Despliegue automatizado de Gaturno en Ubuntu/Debian
#  Uso:  bash deploy.sh [--repo <url_git>] [--branch <rama>]
# =============================================================================
set -euo pipefail

# ── Configuración por defecto (editar según tu repositorio) ─────────────────
REPO_URL="${REPO_URL:-https://github.com/TU_USUARIO/gaturno-vetclinic.git}"
BRANCH="${BRANCH:-main}"
APP_DIR="${APP_DIR:-/opt/gaturno-vetclinic}"

# Parsear argumentos opcionales
while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)   REPO_URL="$2"; shift 2 ;;
    --branch) BRANCH="$2";   shift 2 ;;
    --dir)    APP_DIR="$2";  shift 2 ;;
    *) echo "Opción desconocida: $1"; exit 1 ;;
  esac
done

# ── Colores ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# ── Verificar que se ejecuta como root o con sudo ────────────────────────────
if [[ $EUID -ne 0 ]]; then
  error "Ejecutar como root o con sudo: sudo bash deploy.sh"
fi

info "=== Gaturno — Despliegue iniciado ==="

# ── 1. Instalar dependencias del sistema ─────────────────────────────────────
info "Verificando dependencias del sistema..."

install_if_missing() {
  local cmd="$1" pkg="${2:-$1}"
  if ! command -v "$cmd" &>/dev/null; then
    info "Instalando $pkg..."
    apt-get install -y "$pkg"
  else
    info "$cmd ya está instalado — omitiendo."
  fi
}

apt-get update -qq

install_if_missing git git
install_if_missing curl curl

# Docker
if ! command -v docker &>/dev/null; then
  info "Instalando Docker..."
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
else
  info "Docker ya está instalado — omitiendo."
fi

# Docker Compose (plugin v2)
if ! docker compose version &>/dev/null 2>&1; then
  info "Instalando Docker Compose plugin..."
  apt-get install -y docker-compose-plugin
else
  info "Docker Compose ya está instalado — omitiendo."
fi

info "✓ Dependencias verificadas."

# ── 2. Clonar o actualizar el repositorio ────────────────────────────────────
if [[ -d "$APP_DIR/.git" ]]; then
  info "Repositorio encontrado en $APP_DIR — ejecutando git pull..."
  git -C "$APP_DIR" fetch origin
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull origin "$BRANCH"
else
  info "Clonando repositorio en $APP_DIR..."
  mkdir -p "$(dirname "$APP_DIR")"
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"
info "✓ Código actualizado en $APP_DIR"

# ── 3. Configurar .env de producción ─────────────────────────────────────────
if [[ ! -f "$APP_DIR/.env" ]]; then
  if [[ -f "$APP_DIR/.env.docker" ]]; then
    cp "$APP_DIR/.env.docker" "$APP_DIR/.env"
    warn "⚠  Se creó .env desde .env.docker."
    warn "   EDITA $APP_DIR/.env con los valores reales antes de continuar."
    warn "   Luego vuelve a ejecutar este script."
    exit 0
  else
    error "No se encontró .env ni .env.docker. Crea $APP_DIR/.env manualmente."
  fi
else
  info "✓ .env encontrado."
fi

# ── 4. Construir imágenes Docker ─────────────────────────────────────────────
info "Construyendo imágenes Docker..."
docker compose build --no-cache
info "✓ Imágenes construidas."

# ── 5. Levantar solo la base de datos y esperar que esté lista ───────────────
info "Iniciando base de datos..."
docker compose up -d db
info "Esperando a que PostgreSQL esté listo..."
until docker compose exec -T db pg_isready -q 2>/dev/null; do
  printf '.'
  sleep 2
done
echo
info "✓ PostgreSQL listo."

# ── 6. Ejecutar migraciones de forma segura ───────────────────────────────────
info "Ejecutando migraciones de base de datos..."
docker compose run --rm web python manage.py migrate --noinput
info "✓ Migraciones aplicadas."

# ── 7. Recolectar archivos estáticos ─────────────────────────────────────────
info "Recolectando archivos estáticos..."
docker compose run --rm web python manage.py collectstatic --noinput --clear
info "✓ Static files recolectados."

# ── 8. Levantar todos los servicios en segundo plano ─────────────────────────
info "Levantando todos los servicios..."
docker compose up -d
info "✓ Servicios en ejecución."

# ── 9. Mostrar estado final ───────────────────────────────────────────────────
echo ""
info "=== Despliegue completado ==="
docker compose ps
echo ""
info "La aplicación está disponible en: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
warn "Recordatorio: configura un reverse proxy (Nginx) y HTTPS (Let's Encrypt)"
warn "para exponer la app en producción de forma segura."
