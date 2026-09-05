#!/usr/bin/env bash
# First-time bootstrap: git clone at /srv/apps/bachelor-cookbook on the production host.
# Preserves an existing .env.docker when replacing a non-git tree.
#
# Usage (from repo root, after git push origin main):
#   ./deploy/bootstrap-server.sh
#
# Do not run from a cloud agent VM. Justin’s coordinator bootstraps the host
# after review/CI. This script only documents and automates the laptop → SSH path.
set -euo pipefail

HOST="${BACHELOR_COOKBOOK_DEPLOY_HOST:-root@178.104.205.138}"
APP_DIR="${BACHELOR_COOKBOOK_DEPLOY_DIR:-/srv/apps/bachelor-cookbook}"
REPO="${BACHELOR_COOKBOOK_GIT_REPO:-git@github.com:justinkemersion/bachelor-pressure-cooker-manual.git}"
BRANCH="${BACHELOR_COOKBOOK_DEPLOY_BRANCH:-main}"
COMPOSE_ENV="${BACHELOR_COOKBOOK_COMPOSE_ENV:-.env.docker}"

ssh "$HOST" "set -euo pipefail
  if [ -d '$APP_DIR/.git' ]; then
    echo 'ERROR: $APP_DIR is already a git clone.'
    echo 'Use ./deploy/relaunch.sh for routine deploys.'
    exit 1
  fi

  ENV_BACKUP=''
  if [ -f '$APP_DIR/$COMPOSE_ENV' ]; then
    ENV_BACKUP=\$(mktemp)
    cp '$APP_DIR/$COMPOSE_ENV' \"\$ENV_BACKUP\"
    echo '=== preserved existing $COMPOSE_ENV ==='
  fi

  if [ -d '$APP_DIR' ]; then
    echo '=== removing non-git tree at $APP_DIR ==='
    rm -rf '$APP_DIR'
  fi

  mkdir -p /srv/apps
  echo '=== git clone ==='
  git clone '$REPO' '$APP_DIR'
  cd '$APP_DIR'
  git checkout '$BRANCH'

  if [ -n \"\$ENV_BACKUP\" ] && [ -f \"\$ENV_BACKUP\" ]; then
    cp \"\$ENV_BACKUP\" '$COMPOSE_ENV'
    rm \"\$ENV_BACKUP\"
  elif [ ! -f '$COMPOSE_ENV' ]; then
    cp deploy/env.docker.example '$COMPOSE_ENV'
    echo '=== created $COMPOSE_ENV from example (content-only; no Flux secrets) ==='
    echo '=== then: ./deploy/relaunch.sh ==='
  fi

  echo '=== docker compose up --build -d ==='
  docker compose --env-file '$COMPOSE_ENV' up --build -d
  docker compose --env-file '$COMPOSE_ENV' ps
"

echo "=== smoke test ==="
curl -sS -o /dev/null -w "https bachelor-cookbook.vsl-base.com/health: %{http_code}\n" https://bachelor-cookbook.vsl-base.com/health || true
