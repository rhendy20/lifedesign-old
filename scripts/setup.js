#!/usr/bin/env node
"use strict";

const { execSync } = require("child_process");
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

console.log("Life Design — local setup\n");

if (!fs.existsSync(path.join(root, ".env"))) {
  fs.copyFileSync(path.join(root, ".env.example"), path.join(root, ".env"));
  console.log("Created .env from .env.example");
}

run("pnpm install");
run("pnpm db:up");
run("pnpm db:migrate");
run("pnpm db:seed");

console.log("\nSetup done. Run: pnpm run dev");
