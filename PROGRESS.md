# PROGRESS — Bachelor Cookbook

Another agent can resume from this file.

## Status (2026-09-05)

Read-only Vessel/vsl-base deploy path. Hostname **https://bachelor-cookbook.vsl-base.com**. No Flux, no Auth.js, no tenant DB.

## What is shipped

- Markdown book (`bachelor-cookbook-book/`) is the source of truth.
- Next reader (`bachelor-cookbook-web/`) loads it via `resolveBookRoot()` in `src/lib/content.ts`.
- Local default: sibling `../bachelor-cookbook-book` (cwd = web package).
- Production image: `BOOK_ROOT=/app/bachelor-cookbook-book` (book COPYed into the image).
- Host wiring: root `Dockerfile`, `docker-compose.yml` (Traefik + `flux-network`), `deploy/` helpers.
- `/health` → `{ ok: true, service: "bachelor-cookbook" }`.
- Flux / pantry / prep plans / migrations: **not implemented**. Bookmark: [`docs/FUTURE_FLUX.md`](docs/FUTURE_FLUX.md).

## Host (coordinator only)

Do not SSH-deploy or merge from a cloud agent. After CI is green, Justin’s coordinator:

```
# laptop, after main has these files
cp deploy/env.docker.example deploy/.env.docker
./deploy/bootstrap-server.sh
./deploy/relaunch.sh
```

Checkout on host: `root@178.104.205.138:/srv/apps/bachelor-cookbook`.

## Verify locally (web package)

```
cd bachelor-cookbook-web
npm ci
npm run lint
npm run typecheck
npm test
npm run build
```

`npm test` and `next build` both fail if the sibling book is missing.

## Resume notes

- Do not add `flux.json`, Auth.js, or PostgREST in a “small follow-up” unless asked.
- Do not touch Field Notes or other Vessel apps.
- Do not `flux push` or SSH to the production host from a cloud agent VM.
