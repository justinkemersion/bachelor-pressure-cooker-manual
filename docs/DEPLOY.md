# Deploy Bachelor Cookbook

Production URL: **https://bachelor-cookbook.vsl-base.com**

Read-only markdown reader. Laptop development stays `npm run dev` in `bachelor-cookbook-web/` with the sibling book. Production bakes that book into the Docker image.

**Do not SSH-deploy from a cloud agent.** Justin’s coordinator bootstraps the host after review/CI.

## Topology

| Piece | Value |
|-------|--------|
| App host | `bachelor-cookbook.vsl-base.com` (Traefik + ACME on `flux-network`) |
| App checkout | `/srv/apps/bachelor-cookbook` on `root@178.104.205.138` |
| Git | `git@github.com:justinkemersion/bachelor-pressure-cooker-manual.git`, branch `main` |
| Runtime env | `/srv/apps/bachelor-cookbook/.env.docker` (from `deploy/env.docker.example`) |
| Compose services | `web` (Next only — no worker, no Flux) |
| Book in image | `/app/bachelor-cookbook-book` (`BOOK_ROOT`) |

`*.vsl-base.com` already points at `178.104.205.138`. No DNS ticket.

Production must never load `.env.local`. This phase has no Auth.js or Flux secrets.

Code moves only: commit → push → SSH `git pull` → `docker compose --env-file .env.docker up --build -d`.

## Image layout

Build context is the **monorepo root**. The Dockerfile copies `bachelor-cookbook-web/` into `/app` and `bachelor-cookbook-book/` into `/app/bachelor-cookbook-book`. `next build` and `node server.js` both set `BOOK_ROOT=/app/bachelor-cookbook-book`. Standalone Next output does not include a sibling checkout unless we COPY the book into the runner stage — we do.

## First bootstrap (from Justin’s laptop)

After `main` has the deploy files:

```bash
cp deploy/env.docker.example deploy/.env.docker
# No Flux/Auth secrets to fill this phase.

./deploy/bootstrap-server.sh
./deploy/relaunch.sh
```

If bootstrap created `.env.docker` from the example on the host, relaunch is enough.

## Routine deploy

```bash
git push origin main
./deploy/relaunch.sh
# If branding env changed:
./deploy/sync-env-remote.sh --apply --restart
```

## Health

- App: `https://bachelor-cookbook.vsl-base.com/health` → `{ ok: true, service: "bachelor-cookbook" }`
- Container healthcheck uses the same path
- Served from `bachelor-cookbook-web/src/app/health/route.ts` (public, no auth)

## Rollback

1. On the server: `cd /srv/apps/bachelor-cookbook && git fetch && git checkout <known-good-sha>`
2. `docker compose --env-file .env.docker up --build -d`

## Not this phase

Flux tenant DB, Auth.js, pantry, prep plans: see [`FUTURE_FLUX.md`](FUTURE_FLUX.md).
