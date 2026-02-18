#!/usr/bin/env bash
# Setup local PostgreSQL for Life Design (no Docker).
# Run this in your terminal. Requires Homebrew: https://brew.sh

set -e

echo "Life Design — local PostgreSQL setup"
echo ""

# Check for Homebrew
if ! command -v brew &>/dev/null; then
  echo "Homebrew not found. Install it first:"
  echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  echo ""
  echo "Then add it to PATH (see the install output) and re-run this script."
  exit 1
fi

# Install PostgreSQL 16
if ! command -v psql &>/dev/null; then
  echo "Installing PostgreSQL 16..."
  brew install postgresql@16
  echo "PostgreSQL installed."
else
  echo "PostgreSQL already installed: $(psql --version)"
fi

# Start PostgreSQL
echo ""
echo "Starting PostgreSQL..."
brew services start postgresql@16 2>/dev/null || brew services start postgresql@16

# Wait for it to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 3

# Add to PATH for this session (Homebrew postgresql@16)
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
export PATH="/usr/local/opt/postgresql@16/bin:$PATH"

# Create user and database (DROP+CREATE for idempotency)
echo ""
echo "Creating database and user..."
psql postgres -c "DROP DATABASE IF EXISTS lifedesign;" 2>/dev/null || true
psql postgres -c "DROP USER IF EXISTS lifedesign;" 2>/dev/null || true
psql postgres -c "CREATE USER lifedesign WITH PASSWORD 'lifedesign_local' CREATEDB;"
psql postgres -c "CREATE DATABASE lifedesign OWNER lifedesign;"

echo ""
echo "Done. PostgreSQL is ready."
echo ""
echo "Add USE_LOCAL_POSTGRES=1 to your .env (or create .env.local-postgres)."
echo "Then run: pnpm run local"
