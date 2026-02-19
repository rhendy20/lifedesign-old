# MVP Spec — Life Capture (Tightened)

## Why This Exists

Prove the core daily loop with minimal friction: `record -> transcribe -> review -> save -> revisit`.

If this loop is fast and reliable, Robert will use it daily and we have a foundation to iterate.

## Product Challenge to Original Draft

- Keep this inside the existing Expo mobile app + API stack.
- Do not create a separate web app or IndexedDB path for v1.
- Store entries in existing Postgres via `/reflections` to preserve continuity with current architecture.
- Keep feature scope minimal; polish the core interaction instead of adding new surfaces.

## v1 Scope (Build Now)

1. Capture screen with single primary voice action.
2. Recording states: idle, recording (timer), processing.
3. Transcription review screen with editable text.
4. Save and discard actions.
5. Past entries list and entry detail view.
6. Graceful error states (permission denied, empty transcription, network/transcription failure).

## Explicitly Out of Scope

- AI insights/themes
- Search
- Categories/collections
- Export
- Multi-user/auth hardening
- Analytics/settings

## UX/Performance Targets

1. User can start recording in under 3 seconds from open.
2. Transcription feedback is immediate (`Processing...` state shown).
3. Save action gives visible success confirmation.
4. Capture remains usable even if entries list is still loading.

## Technical Notes

- Mobile: Expo React Native (`apps/mobile`).
- Recording: `expo-av`.
- Haptics: `expo-haptics`.
- Transcription: API `POST /transcriptions` (OpenAI server-side).
- Persistence: API `POST/GET /reflections` (Postgres via Prisma).

## Done When

1. End-to-end flow works on device/emulator: open -> record -> transcribe -> edit -> save -> view entry.
2. Max recording length enforced at 5 minutes with warning around 4:30.
3. Errors never strand the user; each error state has a clear retry path.
