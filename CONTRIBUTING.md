# Contributing to dash-ui

Thanks for considering a contribution. This is a small, focused library — keep
changes scoped and avoid adding dependencies unless they're essential.

## Development setup

```bash
git clone https://github.com/dash-libs/dash-ui.git
cd dash-ui
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest tests/ -v
```

Tests must run without a Spark session or a live Databricks workspace — keep
any Spark/Databricks-specific code inside functions (never at module level)
so `import dashui` and the test suite work in a plain Python environment.

## Linting

```bash
ruff check dashui/
```

CI runs lint → test (Python 3.9–3.12) → build on every PR; all three must pass.

## Making a change

1. Open an issue first for anything beyond a small fix, so we can agree on
   the approach before you write code.
2. Add or update tests for any behavior change.
3. Keep `CLAUDE.md` in sync if you change the module structure or a design
   rule documented there.
4. Open a PR against `main`. The release workflow handles versioning —
   don't bump the version yourself.

## Code style

- No comments explaining *what* code does — names should make that obvious.
  Comment only the *why* when it's genuinely non-obvious.
- Match the existing patterns in `components.py` / `theme.py` rather than
  introducing a new style for new widgets.

## Reporting bugs / requesting features

Use the issue templates in `.github/ISSUE_TEMPLATE/`. For security issues,
see [SECURITY.md](SECURITY.md) instead of opening a public issue.
