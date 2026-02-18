# Local development

Get the Life Design platform running locally in a few minutes.

## Prerequisites

- **Node.js** 18+
- **pnpm** 9+ (`npm install -g pnpm`)
- **Postgres** — either **Docker** or **local PostgreSQL** (see below)
- **Expo Go** on your phone (optional; you can use simulator/emulator)

## Quick start

### 1. Clone and install

```bash
git clone <repo-url>
cd lifedesign
pnpm install
```

### 2. Environment

```bash
cp .env.example .env
# Edit .env if you need different DB credentials or API port.
# Add OPENAI_API_KEY for voice transcription.
```

### 3. Database

**Option A — Docker:**

```bash
pnpm db:up
pnpm db:migrate
pnpm db:seed
```

**Option B — Local PostgreSQL (no Docker):**

```bash
pnpm setup:local-postgres   # One-time: installs Postgres via Homebrew, creates DB/user
# Add USE_LOCAL_POSTGRES=1 to .env
pnpm db:migrate
pnpm db:seed
```

### 4. Start API

```bash
pnpm api
```

API runs at `http://localhost:3000` (or `API_PORT` from `.env`).

Voice transcription endpoint (`POST /transcriptions`) requires `OPENAI_API_KEY`.

### 5. Start mobile app

In a second terminal:

```bash
pnpm mobile
```

- Press `i` for iOS simulator or `a` for Android emulator.
- Or scan the QR code with Expo Go on your device.

**On device:** If the app calls the API, set `EXPO_PUBLIC_API_URL` in `.env` (or in app) to your machine’s LAN IP (e.g. `http://192.168.1.x:3000`). Simulator can use `http://localhost:3000`.

## Useful commands

| Command                     | Description                         |
|-----------------------------|------------------------------------|
| `pnpm setup:local-postgres` | Setup local Postgres (no Docker)   |
| `pnpm db:up`                | Start Postgres (Docker)            |
| `pnpm db:down` | Stop Postgres                  |
| `pnpm db:migrate` | Apply Prisma migrations    |
| `pnpm db:seed` | Seed database                  |
| `pnpm db:studio` | Open Prisma Studio (DB UI)  |
| `pnpm api`     | Run API in dev (watch)         |
| `pnpm mobile`  | Run Expo dev server            |

## Troubleshooting

- **Docker not found:** Use local PostgreSQL instead: `pnpm setup:local-postgres`, add `USE_LOCAL_POSTGRES=1` to `.env`, then `pnpm run local`.
- **Port 5432 in use:** Another Postgres is running. Stop it or change the port in `infra/docker-compose.yml` and `DATABASE_URL`.
- **API connection refused from device:** Use your computer’s LAN IP in `EXPO_PUBLIC_API_URL`, and ensure firewall allows port 3000.
- **Prisma migrate fails:** Ensure `pnpm db:up` has been run and `DATABASE_URL` in `.env` matches `docker-compose.yml` credentials.
