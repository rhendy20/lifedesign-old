# Architecture — Life Design Platform

## High-level

```
Mobile (Expo)  →  API (Fastify)  →  Prisma  →  Postgres
     ↑                   ↑
  Chat-first UI      OAuth (TODO)
```

- **Mobile:** Single Expo app, TypeScript. Chat-first UI with prominent visual elements. Consumes REST API.
- **API:** Fastify, TypeScript. REST for now; auth via OAuth (stubbed in first slice). Prisma for DB.
- **Database:** Postgres in Docker locally; same schema can run on Vercel Postgres or Neon later.

## Monorepo layout

- `apps/mobile` — Expo app.
- `apps/api` — Fastify server, Prisma, routes.
- `packages/shared` — Shared types (e.g. `Reflection`), constants. Used by mobile and API where useful.
- `infra/` — Docker Compose for local Postgres.
- `docs/` — Project brief, architecture, decisions, local dev.

## Data flow (vertical slice)

1. User enters text in chat input and sends.
2. Mobile `POST /reflections` with body `{ content }`. (Auth stubbed: fixed or header-based userId.)
3. API validates, creates row via Prisma, returns reflection.
4. Mobile appends to list and shows in thread.

## Real-time (later)

- **Streaming AI:** API responds with SSE or chunked JSON; mobile consumes stream and updates chat.
- **Sync:** Same user on multiple devices via API (poll or WebSocket) after OAuth.

## Hosting path

- Local: Postgres in Docker, API runs with `pnpm api`, mobile with `pnpm mobile`.
- Later: API and DB can move to Vercel (serverless + Vercel Postgres or Neon) without changing app contract; only `DATABASE_URL` and API base URL change.
