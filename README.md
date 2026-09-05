# The Bachelor Cookbook

A markdown cookbook and a Next.js reader for the bachelor kitchen.

- **Book (source of truth):** `bachelor-cookbook-book/` — fundamentals, techniques, recipes, reference.
- **Reader:** `bachelor-cookbook-web/` — loads that sibling tree via `src/lib/content.ts`.
- **Production:** https://bachelor-cookbook.vsl-base.com — public, **read-only**. No account required.

Flux (auth, pantry, prep plans, tenant DB) is **not** in this repo yet. See [`docs/FUTURE_FLUX.md`](docs/FUTURE_FLUX.md) and [`PROGRESS.md`](PROGRESS.md).

## Local reader

```bash
cd bachelor-cookbook-web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The app expects `../bachelor-cookbook-book` next to the web package.

```bash
npm run lint
npm run typecheck
npm test          # sibling book is visible
npm run build     # also checks internal markdown links
```

## Production (Vessel / vsl-base)

Foundry-style host wiring only: Docker image, compose on external `flux-network`, Traefik `Host(\`bachelor-cookbook.vsl-base.com\`)`.

The image **bakes the book in**. Build context is the monorepo root. Runtime `BOOK_ROOT` is `/app/bachelor-cookbook-book`.

Justin’s coordinator bootstraps the host after CI — agents do not SSH-deploy or merge.

```bash
# laptop, after main has deploy files
cp deploy/env.docker.example deploy/.env.docker
./deploy/bootstrap-server.sh   # first time → /srv/apps/bachelor-cookbook on root@178.104.205.138
./deploy/relaunch.sh           # git pull + docker compose up --build -d
```

Details: [`docs/DEPLOY.md`](docs/DEPLOY.md).

## Constraints

- No secrets in git (`.env`, `.env.local`, `deploy/.env.docker`)
- Code to the host only via git
- Do not add Flux or Auth.js unless a later PR asks for it
