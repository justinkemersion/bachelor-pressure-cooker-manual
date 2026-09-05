# Future: Foundry + Flux product layer

**Status: deferred. Do not implement in this tree until a later PR explicitly asks for it.**

This repository is a public, read-only cookbook: markdown under `bachelor-cookbook-book/` served by `bachelor-cookbook-web/`. Production on Vessel (`https://bachelor-cookbook.vsl-base.com`) is Foundry-style **host wiring only** — Docker, compose, Traefik on `flux-network`. There is no Flux tenant, no `flux.json`, no PostgREST schema, no Auth.js gate on reading the book.

## Intentionally not in this phase

- Auth.js / OAuth (GitHub or otherwise) as a requirement to read pages
- Flux project, gateway JWT, PostgREST schema, or `flux push`
- Tenant DB: pantry, shopping lists, meal / prep plans
- Numbered SQL migrations or Foundry `lib/flux/` client
- MCP or other write surfaces against a private archive

Public GET of `/`, `/health`, and book routes is the product.

## Desired later

A full Foundry + Flux overlay, patterned after Field Notes / Static / `flux-app-foundry`, so a signed-in household can persist:

- pantry and staples
- prep / meal plans
- shopping lists
- per-tenant notes on recipes

That work should start from an explicit product PR: add `flux.json`, fail-closed auth for **writes**, keep the markdown reader public unless product law changes, and never invent Flux-core behavior from this repo.

See also `PROGRESS.md`.
