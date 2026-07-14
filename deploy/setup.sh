#!/usr/bin/env bash
#
# One-shot provisioning for the GSE Tracker on a fresh Ubuntu EC2 instance.
# Installs system deps, builds the frontend, sets up the backend as a systemd
# service behind nginx, and obtains a Let's Encrypt certificate.
#
# Usage (run as the normal 'ubuntu' user, NOT root — it calls sudo itself):
#   git clone https://github.com/AdomBoateng/gse-tracker-bot.git
#   cd gse-tracker-bot
#   bash deploy/setup.sh <domain> <email>
#
# Example:
#   bash deploy/setup.sh gse-tracker.duckdns.org you@example.com
#
set -euo pipefail

DOMAIN="${1:-}"
EMAIL="${2:-}"
if [[ -z "$DOMAIN" || -z "$EMAIL" ]]; then
  echo "Usage: bash deploy/setup.sh <domain> <email>" >&2
  echo "  e.g. bash deploy/setup.sh gse-tracker.duckdns.org you@example.com" >&2
  exit 1
fi

# Repo root = parent of this script's dir.
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_USER="$(whoami)"
echo "==> App dir:   $APP_DIR"
echo "==> Run user:  $RUN_USER"
echo "==> Domain:    $DOMAIN"

# ── 0. Reachability check for the upstream GSE API ────────────────────────────
echo "==> Checking upstream GSE API reachability from this host..."
code="$(curl -m 15 -s -o /dev/null -w '%{http_code}' https://dev.kwayisi.org/apis/gse/live || true)"
if [[ "$code" == "200" ]]; then
  echo "    OK: dev.kwayisi.org returned 200 — live data will work here."
else
  echo "    WARNING: got '$code' (not 200). This AWS IP may be blocked by the"
  echo "    upstream just like Render was. Continuing setup, but if live data is"
  echo "    empty afterwards, the data source is the problem, not the deploy."
fi

# ── 1. System dependencies ────────────────────────────────────────────────────
echo "==> Installing system packages..."
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip nginx curl ca-certificates gnupg

# Node.js 22 (Vite 8 needs >= 20.19 / 22.12) via NodeSource.
if ! command -v node >/dev/null || [[ "$(node -v | cut -d. -f1 | tr -d v)" -lt 20 ]]; then
  echo "==> Installing Node.js 22..."
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
echo "    node $(node -v), npm $(npm -v)"

# certbot via snap (Ubuntu's recommended path).
if ! command -v certbot >/dev/null; then
  echo "==> Installing certbot..."
  sudo snap install core && sudo snap refresh core
  sudo snap install --classic certbot
  sudo ln -sf /snap/bin/certbot /usr/bin/certbot
fi

# ── 2. Backend: venv + deps + env ─────────────────────────────────────────────
echo "==> Setting up backend..."
cd "$APP_DIR/backend"
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt   # gunicorn + uvicorn are pinned here

cat > "$APP_DIR/backend/.env" <<EOF
DEBUG=false
GSE_API_URL=https://dev.kwayisi.org/apis/gse
CORS_ORIGINS=https://$DOMAIN
EOF
echo "    wrote backend/.env"

# ── 3. Frontend: build ────────────────────────────────────────────────────────
# t2.micro has only ~1GB RAM; the vue-tsc + vite build can OOM. Add swap once so
# the build (and future rebuilds) don't get killed.
if ! sudo swapon --show | grep -q '/swapfile'; then
  echo "==> Creating 2G swapfile (guards against OOM on small instances)..."
  sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

echo "==> Building frontend..."
cd "$APP_DIR/frontend"
npm install
npm run build
echo "    built frontend/dist"

# ── 4. systemd service for the backend ────────────────────────────────────────
echo "==> Installing systemd service..."
sed -e "s|__RUN_USER__|$RUN_USER|g" -e "s|__APP_DIR__|$APP_DIR|g" \
  "$APP_DIR/deploy/gse-tracker-api.service.template" \
  | sudo tee /etc/systemd/system/gse-tracker-api.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now gse-tracker-api
sleep 2
sudo systemctl --no-pager --lines=5 status gse-tracker-api || true

# ── 5. nginx site ─────────────────────────────────────────────────────────────
echo "==> Configuring nginx..."
sed -e "s|__DOMAIN__|$DOMAIN|g" -e "s|__APP_DIR__|$APP_DIR|g" \
  "$APP_DIR/deploy/nginx.conf.template" \
  | sudo tee /etc/nginx/sites-available/gse-tracker >/dev/null
sudo ln -sf /etc/nginx/sites-available/gse-tracker /etc/nginx/sites-enabled/gse-tracker
sudo rm -f /etc/nginx/sites-enabled/default
# nginx needs execute (traversal) permission on the home dir path to reach dist.
chmod o+x "$HOME" 2>/dev/null || true
sudo nginx -t
sudo systemctl reload nginx

# ── 6. Let's Encrypt certificate ──────────────────────────────────────────────
echo "==> Requesting Let's Encrypt certificate for $DOMAIN..."
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" --redirect

echo ""
echo "==> Done. Visit: https://$DOMAIN"
echo "    Backend health:   curl http://127.0.0.1:8000/health"
echo "    Live data check:  curl -s http://127.0.0.1:8000/api/v1/gse/live | head -c 120"
echo "    Logs:             sudo journalctl -u gse-tracker-api -f"
echo "    Restart backend:  sudo systemctl restart gse-tracker-api"
