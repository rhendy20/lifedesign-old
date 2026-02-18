#!/usr/bin/env node
"use strict";

const { execSync, spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const envPath = path.join(root, ".env");

function parseEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return {};
  const out = {};
  for (const line of fs.readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const equalsIndex = trimmed.indexOf("=");
    if (equalsIndex <= 0) continue;
    const key = trimmed.slice(0, equalsIndex).trim();
    let value = trimmed.slice(equalsIndex + 1).trim();
    if (
      (value.startsWith("\"") && value.endsWith("\"")) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    out[key] = value;
  }
  return out;
}

function getCommandEnv() {
  return {
    ...process.env,
    ...parseEnvFile(envPath),
  };
}

function run(cmd, opts = {}) {
  console.log("\n>", cmd);
  execSync(cmd, {
    stdio: "inherit",
    cwd: root,
    env: getCommandEnv(),
    ...opts,
  });
}

console.log("Life Design — one-command local run\n");

// Setup once (idempotent)
if (!fs.existsSync(path.join(root, ".env"))) {
  fs.copyFileSync(path.join(root, ".env.example"), path.join(root, ".env"));
  console.log("Created .env from .env.example");
}
run("pnpm install");

// Skip Docker if USE_LOCAL_POSTGRES=1 in .env (or if .env.local-postgres exists)
const useLocalPostgres =
  fs.existsSync(path.join(root, ".env.local-postgres")) ||
  (fs.existsSync(envPath) &&
    fs.readFileSync(envPath, "utf8").includes("USE_LOCAL_POSTGRES=1"));

if (useLocalPostgres) {
  console.log("\nUsing local PostgreSQL (skipping Docker)\n");
} else {
  try {
    run("pnpm db:up");
  } catch (err) {
    console.warn("\nDocker unavailable. Skipping db:up. Use local PostgreSQL (run ./scripts/setup-local-postgres.sh first).\n");
  }
}

run("pnpm db:migrate");
run("pnpm db:seed");

// Start API and mobile together (concurrently prefixes output)
console.log("\nStarting API and mobile app (Ctrl+C to stop both)\n");
const child = spawn("pnpm", ["run", "dev"], {
  cwd: root,
  stdio: "inherit",
  shell: true,
  env: getCommandEnv(),
});
child.on("exit", (code) => process.exit(code ?? 0));
