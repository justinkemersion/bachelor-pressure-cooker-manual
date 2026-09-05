<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Bachelor Cookbook (this package)

Read-only markdown reader. Production: https://bachelor-cookbook.vsl-base.com.

- Book path: `BOOK_ROOT` or sibling `../bachelor-cookbook-book`. Do not assume the book is inside this package.
- Public `/health` and content pages — no Auth.js requirement.
- Do not add Flux (`flux.json`, migrations, PostgREST) here. See `../docs/FUTURE_FLUX.md`.
- Host relaunch: `../deploy/relaunch.sh` → `root@178.104.205.138:/srv/apps/bachelor-cookbook`. Do not SSH-deploy from a cloud agent.
- Repo-level rules: `../AGENTS.md`.

