# Exporting from Claude and Importing into Cursor

This guide covers how to move project context, instructions, and best practices from Claude (claude.ai projects) into Cursor so you can use them with agent commands and rules.

---

## Part 1: Exporting from Claude

Claude doesn’t offer a single “export project” button. You export by copying the pieces that matter.

### Per project in Claude

1. **Project instructions (custom instructions)**  
   - Open the project in [claude.ai](https://claude.ai).  
   - Go to the project **Settings** (gear or project name → settings).  
   - Find **Project instructions** (or “Custom instructions”).  
   - **Copy the full text** into a local file, e.g. `claude-export-<project-name>.md`.

2. **Pinned / referenced documents**  
   - Note which docs you often attach or pin in that project.  
   - For each one: open the doc in Claude or in its original app, then **copy the content** into a file in your repo (e.g. under `docs/` or a folder like `docs/claude-imports/`).  
   - Keep filenames clear so you know which project they came from.

3. **Decisions and conventions**  
   - If you wrote in chat things like “we always do X” or “never do Y,” copy those into a single doc (e.g. `docs/claude-export-<project-name>-decisions.md`) so you can reuse them in Cursor.

### Batch export (multiple projects)

- Create a folder, e.g. `claude-exports/`, and for each project add:
  - `claude-exports/<project-name>-instructions.md` — project instructions.
  - `claude-exports/<project-name>-pinned/` — any pinned/referenced doc contents.
  - `claude-exports/<project-name>-decisions.md` — conventions/decisions (optional).
- You can do this once and then merge the ones you want into Cursor (next section).

---

## Part 2: Importing into Cursor

Cursor uses **rules** (`.cursor/rules/*.mdc`) and **referenced files** (e.g. `@context.md`) to steer agents. Import your Claude content into that structure.

### Option A: Product/vision context (e.g. your Life Design vision)

You already have `context.md` in the repo root. To make sure agents use it:

- **Keep it as a file** and reference it in chat or in prompts: `@context.md`.  
- **Or** turn it into a rule so it’s always considered when relevant:
  - Create `.cursor/rules/life-design-vision.mdc`.
  - Set `alwaysApply: true` if you want it in every conversation, or use a `description` so it’s applied when the topic matches (e.g. product direction, features, UX).
  - Paste the essence of `context.md` (or the full thing) into that rule.

**Recommendation:** Keep `context.md` as the source of truth and add a **short** rule that points to it, e.g. “When discussing product direction, features, or UX, follow the vision and principles in `context.md`.” That keeps rules small and avoids duplication.

### Option B: Per-project instructions from Claude

For each Claude project you care about:

1. **If it’s this repo (Life Design):**  
   - Merge the project instructions into:
     - `.cursor/rules/project.mdc` (coding standards, file ownership), or  
     - a new `.cursor/rules/<name>.mdc` (e.g. `life-design-product.mdc`) for product/UX guidance.  
   - Use the rule frontmatter:
     - `alwaysApply: true` — always in context.  
     - Or `description: "When doing X, do Y"` — applied when the description matches.

2. **If it’s a different project/repo:**  
   - In that repo, create or edit `.cursor/rules/project.mdc` (and optional extra rules) and paste the exported instructions there.  
   - Optionally keep a copy in `docs/` (e.g. `docs/cursor-rules-source.md`) so you can diff and update later.

### Option C: Pinned docs and decisions

- Put exported “pinned” content in `docs/` (e.g. `docs/decisions.md`, `docs/glossary.md`, or `docs/claude-imports/...`).  
- In Cursor, reference them when needed: `@docs/decisions.md`, `@docs/glossary.md`, etc.  
- If something is “always true” for this codebase, add a one-line (or short) mention in `.cursor/rules/project.mdc` so agents pull in that file or behavior (e.g. “Record non-obvious decisions in `docs/decisions.md`”).

---

## Part 3: Using agent commands and best practices in Cursor

- **Agent roles:** Your `AGENTS.md` already defines Orchestrator, Mobile, Backend, Infra, QA. Cursor uses this for multi-step or multi-area work; keep it at the repo root.  
- **Rules:** Anything you want agents to follow by default (language, style, ownership, product principles) should live in `.cursor/rules/*.mdc`.  
- **Context file:** Use `@context.md` (or your vision rule) when you want product/vision context in a chat or when giving a command.  
- **Commands:** You can add custom Cursor commands (e.g. “Plan this feature using AGENTS.md and context.md”) that reference these files explicitly.

---

## Quick checklist

- [ ] Export each Claude project’s **Project instructions** into a `.md` file.
- [ ] Export any **pinned/referenced docs** into `docs/` or `claude-exports/`.
- [ ] For this repo: ensure **context.md** is the vision source; add a small rule in `.cursor/rules/` that references it if you want it applied automatically.
- [ ] Merge Claude **coding/process** instructions into `.cursor/rules/project.mdc` or a new rule.
- [ ] Put **decisions and conventions** into `docs/decisions.md` and reference via rules or `@docs/decisions.md`.
- [ ] Keep **AGENTS.md** at root; use `@AGENTS.md` in chats when you want to remind the agent of roles.

After this, your “agent commands and best practices” in Cursor are: **AGENTS.md** + **.cursor/rules/** + **context.md** (and any other `@`-referenced docs).
