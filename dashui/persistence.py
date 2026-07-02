"""Shared config persistence for every dash-* package.

Every dash-* UI creates/updates some configuration (source configs, monitor
configs, run configs, ...). This module gives them one consistent story for
where that lives:

- If the user has run env_setup() for that library, configs are read/written
  wherever they pointed it — a Workspace path, a Volume, wherever.
- If they haven't, configs default to the directory the notebook is running
  from (`os.getcwd()`), not a hidden home-dir file — so `%pip install` +
  `launch()` with zero setup still persists something findable, right next
  to the notebook.

The "I've run env_setup() for this library" pointer itself always lives in
the same place (home dir) regardless of cwd, so it's discoverable from any
notebook — only the *data* configs default to cwd.
"""
from __future__ import annotations
import json
import os
from pathlib import Path


def _pointer_path(library: str) -> Path:
    return Path.home() / ".dashlibs" / f"{library}_env.json"


def get_config_dir(library: str) -> str:
    """The directory configs for `library` should be read/written from:
    the env_setup()-configured directory if one was set, else cwd."""
    pointer = _pointer_path(library)
    if pointer.exists():
        try:
            configured = json.loads(pointer.read_text()).get("config_dir")
            if configured:
                return configured
        except Exception:
            pass
    return os.environ.get("DASHLIBS_CONFIG_DIR", os.getcwd())


def set_config_dir(library: str, path: str) -> None:
    """Remember `path` as this library's config directory for future sessions."""
    pointer = _pointer_path(library)
    pointer.parent.mkdir(parents=True, exist_ok=True)
    pointer.write_text(json.dumps({"config_dir": path}, indent=2))


def clear_config_dir(library: str) -> None:
    """Forget the configured directory — future calls fall back to cwd again."""
    pointer = _pointer_path(library)
    if pointer.exists():
        pointer.unlink()


def config_path(library: str, name: str = "config") -> str:
    return os.path.join(get_config_dir(library), f"{library}_{name}.json")


def load_config(library: str, name: str = "config", defaults: dict | None = None) -> dict:
    """Read `<config_dir>/<library>_<name>.json`, merged over `defaults`.
    Returns `defaults` (or {}) unchanged if the file doesn't exist or is invalid."""
    path = config_path(library, name)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return {**(defaults or {}), **json.load(f)}
        except Exception:
            pass
    return dict(defaults or {})


def save_config(library: str, config: dict, name: str = "config") -> str:
    """Write `config` to `<config_dir>/<library>_<name>.json`. Returns the path written."""
    path = config_path(library, name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return path
