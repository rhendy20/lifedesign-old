# Architecture Decision Records

Decisions are recorded here. Keep entries short: what was decided, why, and any alternatives considered.

---

## Monorepo with pnpm workspaces

**Decision:** Single repo; `apps/mobile`, `apps/api`, `packages/shared`; pnpm workspaces.

**Why:** One clone, shared types, consistent tooling. pnpm is fast and supports workspace protocol (`workspace:*`).

**Alternatives:** Separate repos (rejected for DX and shared code). Yarn/npm workspaces (pnpm chosen for speed and disk usage).

---

## Expo + React Native for mobile

**Decision:** Expo with React Native and TypeScript for iOS and Android.

**Why:** One codebase, strong DX, OTA updates, straightforward path to app stores. Aligns with “serious product” and significant time investment.

**Alternatives:** Flutter (different language). Native (two codebases).

---

## Fastify for API

**Decision:** Node.js + Fastify + TypeScript.

**Why:** Same language as mobile, low ceremony, good support for streaming (SSE/chunked) for future AI. Easy to host anywhere.

**Alternatives:** Express (more familiar but heavier). tRPC (deferred until shared types become painful).

---

## Postgres + Prisma

**Decision:** Postgres in Docker locally; Prisma as ORM. Design for hosted Postgres (Vercel Postgres, Neon) later.

**Why:** Prisma gives type-safe access, migrations, and a single connection string to swap for production. Postgres is standard and well-supported.

**Alternatives:** SQLite (simpler but different production path). Raw SQL (rejected for maintainability).

---

## REST first (no tRPC in v1)

**Decision:** REST for API in the first slice. Revisit tRPC if shared types and endpoints grow.

**Why:** Simplicity; easy to reason about and debug. tRPC can be added later if duplication or type drift becomes an issue.

---

## OAuth only (no email/password in v1)

**Decision:** Auth via OAuth (Apple, Google). No custom email/password initially.

**Why:** Better mobile UX; fewer moving parts. Email/password can be added later if needed.

---

## First vertical slice: reflections

**Decision:** One table (`Reflection`), `POST/GET /reflections`, one chat-style screen. Auth stubbed (e.g. fixed userId or header).

**Why:** Proves full loop (mobile → API → DB) and matches core use case (capture + later AI). OAuth in next slice.

---

## Chat-first UI with prominent visuals

**Decision:** Conversation at center; at least one distinctive visual element (e.g. header, cards, accent) so it doesn’t look like generic chat.

**Why:** Aligns with product vision (reflection + AI) and differentiates the app.

---

## Speech-first capture with server-side transcription

**Decision:** First journaling interaction is voice-first (`record -> transcribe -> review -> save`), while preserving text input as fallback. Audio is uploaded to API and transcribed server-side (`POST /transcriptions`) using OpenAI.

**Why:** Fastest path to daily low-friction capture without premature complexity. Server-side transcription keeps API keys off device and lets us swap providers later. Manual review before save preserves agency and data quality.
