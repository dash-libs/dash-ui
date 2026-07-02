# CLAUDE.md — dash-ui

Part of the **Dashlibs** suite. See ~/dashlibs for the full context.

Full suite-wide context (release process gotchas, PR/review norms, repo list):
see `~/dashlibs/CLAUDE.md`.

## Purpose
Shared `ipywidgets` component library so every `dash-*` notebook UI looks and
behaves consistently. components.py=widgets (header/source_selector/output_panel/...),
theme.py=design tokens (per-library accent colors + the shared neutral palette),
schema.py=UC column introspection.

**Visual design changed 2026-07-02**: repointed from the datapal-access
Databricks App to Databricks' own product UI (Inter, "Lava" red-orange
`#FF3621` reserved for primary actions only, small 3-6px radii, dense
13px-base forms, underline-style tabs, bordered/hoverable tables) —
explicit user direction ("closer to Databricks native UI", "more tabular
style configs"). Not a pixel-exact extraction (no live workspace to sample
from in this environment) — see theme.py's docstring for what it's
actually grounded in. If you have reference screenshots of the real
Databricks workspace UI, treat those as higher-authority than the current
tokens and re-derive.

New: `editable_table()` in components.py — an add/remove-row key-value
grid (Databricks' own pattern for job parameters / cluster tags / env
vars), for any config that's naturally tabular instead of a free-text
"key=value, key=value" field. Prefer this over a Textarea whenever a
dash-* UI needs a variable-length list of key/value pairs.

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
