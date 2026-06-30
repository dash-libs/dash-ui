# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses patch-only [semantic versioning](https://semver.org/)
bumps via the automated release workflow.

## [Unreleased]

### Changed
- Visual redesign based on the datapal-access Databricks App design system
  (IBM Plex Sans, teal primary, rounded-lg cards with a soft shadow)

## [0.1.2] - 2026-06-30

### Fixed
- Release workflow now uses a `RELEASE_TOKEN` PAT instead of the default
  `GITHUB_TOKEN`, since GITHUB_TOKEN-authored pushes don't trigger
  downstream workflow runs (the release PR's required CI check never ran)
- Added the `LICENSE` file (was referenced by the README badge but missing)

## [0.1.1] - 2026-06-30

### Changed
- Renamed the PyPI distribution to `dash-uis` — `dash-ui` was already taken
  by an unrelated package. The importable module is still `dashui`.

### Fixed
- `hatch version patch` now works (switched from a static to a dynamic
  version sourced from `dashui/__init__.py`)
- Hatchling can now find the wheel's package directory (explicit
  `packages = ["dashui"]` instead of relying on name-matching heuristics)

## [0.1.0] - 2026-06-30

### Added
- Initial release: `header`, `source_selector`, `action_button`,
  `output_panel`, `running_list`, `status_line`, `card`
- `list_columns` / `list_columns_safe` UC table schema introspection
- Per-library accent color theme
