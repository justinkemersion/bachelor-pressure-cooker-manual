Next.js reader for the Bachelor Cookbook markdown book.

The book lives in the sibling directory `../bachelor-cookbook-book`. Local `npm run dev` / `npm run build` load it from there. Production Docker sets `BOOK_ROOT=/app/bachelor-cookbook-book` and bakes that tree into the image. See the repo-root [README](../README.md) and [docs/DEPLOY.md](../docs/DEPLOY.md).

This surface is **read-only**. Flux (auth, pantry, prep plans) is deferred — [docs/FUTURE_FLUX.md](../docs/FUTURE_FLUX.md).

## Getting Started

From this directory, with the book checkout next to it:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

Production host: https://bachelor-cookbook.vsl-base.com — relaunch notes at the repo root (`./deploy/relaunch.sh` on `root@178.104.205.138` under `/srv/apps/bachelor-cookbook`). Cloud agents do not SSH-deploy.
