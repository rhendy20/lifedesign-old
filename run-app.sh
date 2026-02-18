#!/bin/bash
# Run the Life Design app. Use this after you've done first-time setup (Node, pnpm, Docker).
# In Terminal:  cd /Users/roberthenderson/Desktop/lifedesign  then  ./run-app.sh

set -e
cd "$(dirname "$0")"

if ! command -v pnpm &> /dev/null; then
  echo "pnpm is not installed. Run:  npm install -g pnpm"
  echo "See README.md → First-time setup for full instructions."
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo "Node.js is not installed. Install it from https://nodejs.org (LTS)."
  exit 1
fi

echo "Starting Life Design app..."
pnpm run local
