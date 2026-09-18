# Life Design Platform

Life design platform that helps you become more through self-knowledge, character development, and action. Chat-first mobile app + API + local Postgres.

## Defining Experiences insight engine (research run, 2026-09-18)

An unattended run built and evaluated the insight engine behind the Defining Experiences flow. Start with
[FINDINGS.md](FINDINGS.md) (the answer and the disconfirming evidence), then [DECISION.md](DECISION.md) (what to build next),
then [INSIGHTS.md](INSIGHTS.md) (the ten best insights it produced, verbatim). The prototype runs in one command:

```bash
python3 prototype/run.py path/to/my_experiences/
```

See [prototype/README.md](prototype/README.md), [prompts/CHANGELOG.md](prompts/CHANGELOG.md), [eval/README.md](eval/README.md),
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) and [PROGRESS.md](PROGRESS.md). Robert's own transcripts and sealed files were not
available to the run; see FINDINGS.md for what that means.

---

## First-time setup (do this once)

You need three things installed: **Node.js**, **pnpm**, and **Docker**.

### 1. Install Node.js (18 or newer)

- Go to [https://nodejs.org](https://nodejs.org) and download the **LTS** version.
- Run the installer. When it’s done, **close and reopen Terminal** (or Cursor’s terminal).

Check it worked:

```bash
node -v
```

You should see something like `v20.x.x`.

### 2. Install pnpm

In Terminal (or Cursor’s integrated terminal), run:

```bash
npm install -g pnpm
```

Check it worked:

```bash
pnpm -v
```

### 3. Install Docker

- Go to [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
- Download **Docker Desktop** for Mac, install it, and open it. Wait until it says Docker is running (whale icon in the menu bar).

---

## Run the app

1. Open **Terminal** (or the **Terminal** panel in Cursor: View → Terminal).
2. Go to the project folder:

   ```bash
   cd /Users/roberthenderson/Desktop/lifedesign
   ```

3. Run the app (one command):

   ```bash
   pnpm run local
   ```

The first time this will: install dependencies, create `.env`, start Postgres, run migrations, and seed the database. Then it starts the API and the mobile app.

- **API:** [http://localhost:3000](http://localhost:3000)
- **Mobile:** In the same terminal you’ll see a QR code and options. Press **`i`** for iOS simulator or **`a`** for Android emulator, or scan the QR code with the **Expo Go** app on your phone.

To stop everything, press **Ctrl+C** in that terminal. To run again later, use the same command: `pnpm run local`.

---

## Run everything locally (one command, after setup)

**Prerequisites:** Node 18+, pnpm 9+, Docker. Then from the project root:

```bash
pnpm run local
```

This will install deps, create `.env` if needed, start Postgres, run migrations, seed the DB, then start the API and the mobile app in one terminal. Use **Ctrl+C** to stop both.  
To run again later, same command: `pnpm run local`.

---

## Quick start (manual steps)

**Prerequisites:** Node 18+, pnpm 9+, Docker.

```bash
# Clone and install
git clone <repo-url>
cd lifedesign
pnpm install

# Environment
cp .env.example .env
# Add OPENAI_API_KEY to enable voice transcription

# Database
pnpm db:up
pnpm db:migrate
pnpm db:seed

# Terminal 1: API
pnpm api

# Terminal 2: Mobile
pnpm mobile
```

- API: [http://localhost:3000](http://localhost:3000)
- Mobile: press `i` (iOS simulator) or `a` (Android emulator), or scan QR with Expo Go.  
  On a physical device, set `EXPO_PUBLIC_API_URL` in `.env` to your machine’s LAN IP (e.g. `http://192.168.1.x:3000`).

## Repo structure

| Path | Purpose |
|------|--------|
| `apps/mobile` | Expo (React Native) app — chat-first reflections |
| `apps/api` | Fastify API — REST, Prisma, Postgres |
| `packages/shared` | Shared TypeScript types |
| `infra/` | Docker Compose (Postgres) |
| `docs/` | [Project brief](docs/project-brief.md), [architecture](docs/architecture.md), [decisions](docs/decisions.md), [local dev](docs/local-dev.md) |

## Commands

| Command | Description |
|---------|-------------|
| **`pnpm run local`** | **Setup + start API and mobile (one command)** |
| `pnpm run setup` | Install deps, .env, DB up, migrate, seed (no servers) |
| `pnpm run dev` | Start API and mobile only (after setup) |
| `pnpm db:up` | Start Postgres (Docker) |
| `pnpm db:down` | Stop Postgres |
| `pnpm db:migrate` | Run Prisma migrations |
| `pnpm db:seed` | Seed dev data |
| `pnpm db:studio` | Open Prisma Studio |
| `pnpm api` | Run API (watch) |
| `pnpm mobile` | Run Expo dev server |

## First vertical slice

- **DB:** `Reflection` table (id, userId, content, createdAt).
- **API:** `GET /reflections`, `POST /reflections` (auth stubbed as `dev-user-1`).
- **Transcription:** `POST /transcriptions` (multipart audio -> text via OpenAI).
- **Mobile:** Voice-first flow (record -> transcribe -> review -> save) plus past-entry list/detail.

OAuth and streaming AI are planned for later slices.

## Docs

- [Project brief](docs/project-brief.md) — pitch, users, scope
- [Architecture](docs/architecture.md) — high-level and data flow
- [Decisions](docs/decisions.md) — ADRs
- [Local dev](docs/local-dev.md) — setup and troubleshooting

## Agent roles

See [AGENTS.md](AGENTS.md) for Orchestrator, Mobile, Backend, Infra, and QA roles and when to use them.
