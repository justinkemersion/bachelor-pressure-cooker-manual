#!/usr/bin/env bash
# Sync local deploy/.env.docker → production /srv/apps/bachelor-cookbook/.env.docker.
#
# Content-only: the example has public branding + BOOK_ROOT. There are no Flux
# or Auth.js secrets to fill. Dry-run by default; pass --apply to write.
#
# Usage (from repo root):
#   ./deploy/sync-env-remote.sh              # dry-run
#   ./deploy/sync-env-remote.sh --apply      # write remote file
#   ./deploy/sync-env-remote.sh --apply --restart
#
# Env overrides:
#   BACHELOR_COOKBOOK_DEPLOY_HOST   default root@178.104.205.138
#   BACHELOR_COOKBOOK_DEPLOY_DIR    default /srv/apps/bachelor-cookbook
#   BACHELOR_COOKBOOK_LOCAL_ENV     default deploy/.env.docker
#
set -euo pipefail

HOST="${BACHELOR_COOKBOOK_DEPLOY_HOST:-root@178.104.205.138}"
APP_DIR="${BACHELOR_COOKBOOK_DEPLOY_DIR:-/srv/apps/bachelor-cookbook}"
LOCAL_ENV="${BACHELOR_COOKBOOK_LOCAL_ENV:-deploy/.env.docker}"
REMOTE_ENV_NAME=".env.docker"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

show_help() {
  sed -n '2,20p' "$0" | sed 's/^# \?//'
}

APPLY=0
RESTART=0
REMOTE_OVERRIDE=""
for a in "$@"; do
  case "$a" in
    -h | --help)
      show_help
      exit 0
      ;;
    --apply)
      APPLY=1
      ;;
    --restart)
      RESTART=1
      ;;
    *)
      if [[ -n "${REMOTE_OVERRIDE}" ]]; then
        echo "Unexpected extra argument: $a (expected at most one user@host)" >&2
        exit 1
      fi
      REMOTE_OVERRIDE="$a"
      ;;
  esac
done

REMOTE="${REMOTE_OVERRIDE:-$HOST}"
if [[ "$REMOTE" != *"@"* ]]; then
  echo "Invalid ssh target (expected user@host): '$REMOTE'" >&2
  exit 1
fi

LOCAL_PATH="$REPO_ROOT/$LOCAL_ENV"
if [[ ! -f "$LOCAL_PATH" ]]; then
  echo "ERROR: local env file missing: $LOCAL_ENV" >&2
  echo "Copy deploy/env.docker.example → deploy/.env.docker (no secrets required this phase)." >&2
  exit 1
fi

echo "=== local keys in $LOCAL_ENV ==="
grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$LOCAL_PATH" | cut -d= -f1 | sort || true

if grep -Eq '^(FLUX_|AUTH_|NEXTAUTH_)' "$LOCAL_PATH"; then
  echo "WARN: Flux/Auth keys are present. This phase is content-only; they are unused." >&2
fi

if [[ "$RESTART" -eq 1 && "$APPLY" -eq 0 ]]; then
  echo "ERROR: --restart requires --apply" >&2
  exit 1
fi

RSYNC_OPTS=(-avz)
if [[ "$APPLY" -eq 0 ]]; then
  RSYNC_OPTS+=(-n)
  echo ""
  echo "=== DRY RUN (no files written on remote). Pass --apply to sync. ==="
  echo "  remote: $REMOTE"
  echo "  source: $LOCAL_ENV"
  echo "  dest:   $APP_DIR/$REMOTE_ENV_NAME"
else
  echo ""
  echo "=== APPLY: writing $REMOTE:$APP_DIR/$REMOTE_ENV_NAME ==="
fi

ssh "$REMOTE" "test -d '$APP_DIR' || { echo 'ERROR: missing $APP_DIR — run ./deploy/bootstrap-server.sh first' >&2; exit 1; }"

rsync "${RSYNC_OPTS[@]}" "$LOCAL_PATH" "${REMOTE}:${APP_DIR}/${REMOTE_ENV_NAME}"

if [[ "$APPLY" -eq 1 ]]; then
  ssh "$REMOTE" "chmod 600 '$APP_DIR/$REMOTE_ENV_NAME'"
  echo "=== remote keys (names only) ==="
  ssh "$REMOTE" "grep -E '^[A-Za-z_][A-Za-z0-9_]*=' '$APP_DIR/$REMOTE_ENV_NAME' | cut -d= -f1 | sort"
fi

if [[ "$APPLY" -eq 0 ]]; then
  echo ""
  echo "Dry run complete. Re-run with --apply after reviewing."
  exit 0
fi

if [[ "$RESTART" -eq 1 ]]; then
  echo "=== recreate container with new env ==="
  ssh "$REMOTE" "set -euo pipefail
    cd '$APP_DIR'
    docker compose --env-file '$REMOTE_ENV_NAME' up -d --force-recreate
    docker compose --env-file '$REMOTE_ENV_NAME' ps
  "
  echo "Synced and restarted. Smoke: curl -sS https://bachelor-cookbook.vsl-base.com/health"
else
  echo ""
  echo "Synced. Recreate the container to pick up env changes:"
  echo "  ./deploy/relaunch.sh"
  echo "  # or: ./deploy/sync-env-remote.sh --apply --restart"
fi
