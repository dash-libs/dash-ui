# CLAUDE.md — dash-ui

Part of the **Dashlibs** suite. See ~/dashlibs for the full context.

## Purpose
Shared `ipywidgets` component library so every `dash-*` notebook UI looks and
behaves consistently. components.py=widgets (header/source_selector/output_panel/...),
theme.py=per-library accent colors, schema.py=UC column introspection.

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
- `release.yml`— Monday 09:00 UTC: patch bump + GitHub release
