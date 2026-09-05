# Agent rules — Bachelor Cookbook

Monorepo: markdown book (`bachelor-cookbook-book/`) + Next reader (`bachelor-cookbook-web/`).

## Product

1. **Read-only this phase.** Anyone can read the book. Do not add Auth.js, OAuth, or a login wall on content or `/health`.
2. **Do not wire Flux.** No `flux.json`, migrations, PostgREST, or tenant DB. Desired later: [`docs/FUTURE_FLUX.md`](docs/FUTURE_FLUX.md).
3. **Do not touch Field Notes or other Vessel apps.**

## Book path

4. `bachelor-cookbook-web/src/lib/content.ts` resolves the book via `BOOK_ROOT` or the sibling `../bachelor-cookbook-book`. Production Docker sets `BOOK_ROOT=/app/bachelor-cookbook-book` and COPYs the book into the image. Do not point production at a host bind-mount of the checkout unless a later change says so.

## Deploy

5. Host: `root@178.104.205.138`, checkout `/srv/apps/bachelor-cookbook`, URL `https://bachelor-cookbook.vsl-base.com`.
6. Routine rebuild: `./deploy/relaunch.sh` from a laptop after `git push origin main`. Cloud agents do not SSH-deploy or merge.
7. No secrets required for this content-only image. Copy `deploy/env.docker.example` → `.env.docker` on the host.

## Web package (Next.js)

See `bachelor-cookbook-web/AGENTS.md` for Next 16 API rules. Run lint / typecheck / test / build from `bachelor-cookbook-web/`.
