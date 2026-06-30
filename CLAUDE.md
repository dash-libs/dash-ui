# CLAUDE.md — dash-ui

Part of the **Dashlibs** suite. See ~/dashlibs for the full context.

Full suite-wide context (release process gotchas, PR/review norms, repo list):
see `~/dashlibs/CLAUDE.md`.

## Purpose
Shared `ipywidgets` component library so every `dash-*` notebook UI looks and
behaves consistently. components.py=widgets (header/source_selector/output_panel/...),
theme.py=design tokens (per-library accent colors + the shared neutral palette),
schema.py=UC column introspection.

Visual design is modeled on the **datapal-access** Databricks App
(`~/datapal-access` — React + Tailwind + shadcn/ui): IBM Plex Sans, a teal
primary (`#2A9D90`), `rounded-lg` cards with a soft shadow. Tokens were
extracted from `src/index.css` / `tailwind.config.ts` there. If that app's
design system changes, re-extract rather than guessing new values.

PyPI distribution name is **`dash-uis`** (`dash-ui` was taken by an
unrelated package) — the import name (`dashui`) is unaffected. Don't
"fix" this back to `dash-ui` anywhere; it's permanent.

## Structure
- `/components.py` — the widget building blocks
- `/theme.py`       — accent color per library + neutral palette
- `/schema.py`       — `list_columns` / `list_columns_safe` for UC tables
- `tests/`           — pytest, no Spark dependency for unit tests

## Key Design Rules
- Never import Spark at module level — always inside functions
- No business logic here — pure presentation/introspection helpers, consumed
  by other dash-* packages' `ui.py` files
- Every widget factory must work standalone (no global state) so multiple
  `dash-*` UIs can be displayed in the same notebook without colliding

## CI
- `ci.yml`    — PR gate: lint → test → build
- `daily.yml` — 06:00 UTC: tests + .health/log.txt commit
- `release.yml`— Monday 09:00 UTC: patch bump (via a release PR) + GitHub release + PyPI

## Working norms
- **Every change goes through a PR with real human review before merging —
  no exceptions**, including small fixes and including the release
  workflow's own version-bump commit. Don't self-merge, don't push directly
  to `main`, even though this repo currently has no branch protection
  technically enforcing it.
- Prefer small, targeted commits/PRs over large batched ones.
