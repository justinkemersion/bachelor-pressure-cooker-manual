#!/usr/bin/env bash
# Pull latest main and rebuild Bachelor Cookbook on the production host.
# Usage (from repo root, after git push origin main):
#   ./deploy/relaunch.sh
#   ./deploy/relaunch.sh --sync-env   # (optional) push deploy/.env.docker first
#
# Host: root@178.104.205.138
# Checkout: /srv/apps/bachelor-cookbook
# URL: https://bachelor-cookbook.vsl-base.com
#
# Read-only content image. No flux push, no migrations, no Auth.js secrets.

set -euo pipefail

HOST="${BACHELOR_COOKBOOK_DEPLOY_HOST:-root@178.104.205.138}"
APP_DIR="${BACHELOR_COOKBOOK_DEPLOY_DIR:-/srv/apps/bachelor-cookbook}"
BRANCH="${BACHELOR_COOKBOOK_DEPLOY_BRANCH:-main}"
COMPOSE_ENV="${BACHELOR_COOKBOOK_COMPOSE_ENV:-.env.docker}"
CHECK_URL="${BACHELOR_COOKBOOK_CHECK_URL:-https://bachelor-cookbook.vsl-base.com/health}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SYNC_ENV=0
for a in "$@"; do
  case "$a" in
    --sync-env) SYNC_ENV=1 ;;
    -h | --help)
      sed -n '2,16p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown argument: $a (supported: --sync-env)" >&2; exit 1 ;;
  esac
done

if [[ "$SYNC_ENV" -eq 1 ]]; then
  if [[ -x "$SCRIPT_DIR/sync-env-remote.sh" ]]; then
    echo "=== sync env (apply) ==="
    "$SCRIPT_DIR/sync-env-remote.sh" --apply
  else
    echo "ERROR: sync-env-remote.sh not present; run without --sync-env" >&2
    exit 1
  fi
fi

echo "=== ssh redeploy ==="
ssh "$HOST" "set -euo pipefail
  cd '$APP_DIR'

  if [ ! -f '$COMPOSE_ENV' ]; then
    echo 'ERROR: missing $COMPOSE_ENV in $APP_DIR'
    echo 'Copy deploy/env.docker.example → .env.docker (content-only; no Flux secrets).'
    exit 1
  fi

  if [ ! -d .git ]; then
    echo 'ERROR: $APP_DIR is not a git repository.'
    echo 'Run ./deploy/bootstrap-server.sh once first.'
    exit 1
  fi

  git fetch origin '$BRANCH'
  git checkout '$BRANCH'
  git pull --ff-only origin '$BRANCH'

  echo '=== docker compose rebuild ==='
  docker compose --env-file '$COMPOSE_ENV' up --build -d

  echo '=== container status ==='
  docker compose --env-file '$COMPOSE_ENV' ps

  echo '=== health (after brief wait) ==='
  sleep 20
  docker inspect bachelor-cookbook-web --format 'Health: {{.State.Health.Status}} | Running: {{.State.Running}}' 2>/dev/null || true

  echo '=== recent runtime logs ==='
  docker compose --env-file '$COMPOSE_ENV' logs --tail=20 web 2>&1
"

echo "=== smoke test ==="
curl -sS -o /dev/null -w "http: %{http_code}\n" http://bachelor-cookbook.vsl-base.com/ || true
curl -sS -o /dev/null -w "https: %{http_code}\n" "$CHECK_URL" || true
