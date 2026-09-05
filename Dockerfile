# syntax=docker/dockerfile:1
# Bachelor Cookbook at https://bachelor-cookbook.vsl-base.com
# Production image — build from the monorepo root so the markdown book is in context.
#   docker compose --env-file .env.docker build
#
# Layout in the image:
#   /app                         Next app (flattened from bachelor-cookbook-web/)
#   /app/bachelor-cookbook-book  baked markdown source of truth
# Runtime and `next build` both use BOOK_ROOT=/app/bachelor-cookbook-book.
#
# This phase is read-only content. No Flux, Auth.js, or tenant secrets.

FROM node:22-bookworm-slim AS base
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

FROM base AS deps
WORKDIR /app
COPY bachelor-cookbook-web/package.json bachelor-cookbook-web/package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY bachelor-cookbook-web/ ./
COPY bachelor-cookbook-book ./bachelor-cookbook-book

ARG NEXT_PUBLIC_APP_NAME=Bachelor Cookbook
ARG NEXT_PUBLIC_APP_URL=https://bachelor-cookbook.vsl-base.com

ENV NEXT_TELEMETRY_DISABLED=1 \
  NEXT_PUBLIC_APP_NAME=${NEXT_PUBLIC_APP_NAME} \
  NEXT_PUBLIC_APP_URL=${NEXT_PUBLIC_APP_URL} \
  BOOK_ROOT=/app/bachelor-cookbook-book

RUN node scripts/verify-book.mjs && npm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production \
  NEXT_TELEMETRY_DISABLED=1 \
  PORT=3000 \
  HOSTNAME=0.0.0.0 \
  BOOK_ROOT=/app/bachelor-cookbook-book

RUN groupadd --system --gid 1001 nodejs \
  && useradd --system --uid 1001 --gid nodejs nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/bachelor-cookbook-book ./bachelor-cookbook-book

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "server.js"]
