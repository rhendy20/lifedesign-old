# Agent roles — Life Design Platform

One orchestrator coordinates work; sub-agents handle domain-specific implementation. Use this to decide who does what.

## Orchestrator

- **Owns:** Plan, sequencing, and cross-cutting decisions.
- **Does:** Breaks work into tasks, delegates to Mobile / Backend / Infra / QA, and integrates results. Does **not** implement full vertical slices alone (e.g. both API and mobile for one feature); instead coordinates the right agents.
- **When to use:** Any multi-step or multi-area task (new feature, refactor across app + API, onboarding).

## Mobile Agent

- **Owns:** UI, navigation, state, chat-first screens, and visual design in `apps/mobile`.
- **Does:** Expo/React Native components, screens, styling, local state, API calls from the app. Keeps chat-first UX and prominent visual elements in mind.
- **When to invoke:** Mobile-only work (e.g. “style the chat input”, “add a new screen”, “fix layout”).

## Backend Agent

- **Owns:** API routes, auth, DB access, and streaming in `apps/api`.
- **Does:** Fastify routes, Prisma usage, validation, OAuth wiring. Does not change Prisma schema or migrations without alignment (see Database agent / decisions).
- **When to invoke:** API-only work (e.g. “add endpoint X”, “add auth middleware”, “stream response”).

## Infra Agent

- **Owns:** Docker, env, scripts, and local-dev runbooks.
- **Does:** `infra/docker-compose.yml`, root/API scripts, `.env.example`, and `docs/local-dev.md`. Keeps “fresh clone works in a few minutes” true.
- **When to invoke:** “Get DB running”, “add a script”, “document setup”, “prepare for Vercel”.

## QA Agent

- **Owns:** Tests and edge cases.
- **Does:** Jest for API, React Native Testing Library for mobile; regression and boundary cases. Does not block small changes with unnecessary tests.
- **When to invoke:** “Add tests for X”, “regression before release”, “edge cases for auth”.

---

## When to spin up sub-agents

- **Cross-cutting feature** (e.g. “add a reflection and persist it”): Orchestrator coordinates; Backend implements API + DB usage; Mobile implements screen and API call. Orchestrator wires and reviews.
- **Single domain** (e.g. “style the chat input”): Mobile agent only. No need to involve Backend or QA unless tests are requested.
- **Tiny edits, docs-only, dependency bumps:** Orchestrator or a single agent. No need to spin up multiple agents.

## When not to

- One-line fixes, comment updates, or dependency version bumps: handle inline.
- Pure documentation: Orchestrator or Infra.
- Choosing stack or high-level design: Orchestrator; record in `docs/decisions.md`.
