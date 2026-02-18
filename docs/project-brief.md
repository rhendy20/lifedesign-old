# Project Brief — Life Design Platform

## One-sentence pitch

Life design platform that helps you become more through self-knowledge, character development, and action.

## Target users

You (Robert) first; then others as proof of concept.

## Core use case

1. **Capture and organize life design data** — values, priorities, patterns, growth areas.
2. **AI-guided reflection** — intentional questions that push your thinking.

The first vertical slice combines both: a chat-first screen where you can send reflections and (later) receive AI-driven questions, with data persisted via the API.

## Scope

Serious about turning this into a product. Build for daily use and eventual multi-user.

## Decisions summary

| Dimension    | Decision |
|-------------|----------|
| Platform    | iOS and Android (Expo) |
| Mobile stack| Expo + React Native + TypeScript |
| UI          | Chat-first with prominent, distinctive visual elements |
| Backend     | Yes — sync across devices, future multi-user |
| Data        | Real-time (streaming AI, live updates) when needed |
| Database    | Postgres locally (Docker); design for Vercel/Neon later |
| Auth        | OAuth (Apple, Google) from the start |
| Language    | TypeScript only (mobile + API) |
| Time        | Significant per week (part-time or more) |

## Success criteria

- You use it daily because it helps you become more.
- Local dev works from a fresh clone in a few minutes.
- One end-to-end flow (e.g. send reflection → API → DB → show in app) works before adding more features.
