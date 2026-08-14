# AGENTS.md

## Cursor Cloud specific instructions

This repo holds two separate products:

1. **Gated Progressive Formalization operator toolkit** (repo root: `docs/`, `templates/`,
   `applications/`, `locks/`, `exemplars/`, `TRACKER_*.md`, `workflow.md`). This is a
   Markdown methodology toolkit — there is **no build, server, test suite, or package**.
   Live decisions happen through an in-chat picker inside Cursor. `ui/choice-presenter/`
   is an optional static `index.html` + `catalog.json` demo opened via `file://` (no build,
   no dependencies). Nothing here needs environment setup.

2. **`golf-offshoot/`** — the only runnable code. A Python ≥3.10 CLI + library for
   uncertainty-aware golf analysis. It has **no long-running server, database, or
   containers**; it's a CLI that (for real runs) fetches from external HTTP APIs and caches
   to disk. Standard commands live in `golf-offshoot/README.md` and `golf-offshoot/pyproject.toml`.

### Working in `golf-offshoot`

- Dependencies are installed into the **system Python** via
  `pip install --break-system-packages -e ".[dev]"` (the startup update script does this).
  There is no virtualenv. Ubuntu's Python is externally managed, so `--break-system-packages`
  is required and `python3 -m venv` is unavailable unless `python3.12-venv` is installed.
- Console scripts (`golf-offshoot`, `pytest`) install to `~/.local/bin`, which is **not on
  PATH**. Invoke tools as modules instead: `python3 -m golf_offshoot <cmd>` and
  `python3 -m pytest`. Run all commands from the `golf-offshoot/` directory.
- **Tests:** `cd golf-offshoot && python3 -m pytest` — runs fully offline on mock data
  (external feed loading is skipped under pytest). ~96 pass, a few skipped.
- **Lint:** none configured (no ruff/flake8/black/mypy/CI anywhere in the repo).
- **Build:** `python3 -m build` works (needs the `build` package). Not part of normal dev.
- **Run (offline, no network):** `demo`, `explain`, `strategy`, `board` print an
  `OFFLINE DEMO — MOCK DATA` banner and work with no secrets. Good for smoke-testing.
- **Run (real / end-to-end):** `ingest`, `live`, `calibrate`, `pressure-test`,
  `paper-*` need outbound network to external feeds (ESPN, PGA Tour GraphQL, Open-Meteo).
  An odds book is optional: set `THE_ODDS_API_KEY` in `golf-offshoot/.env` (copy from
  `.env.example`) for Hard Rock Bet, or use the keyless Bovada fallback (`--book auto`).
  The system **never auto-bets** — it only produces ranked tables and paper ledgers.
