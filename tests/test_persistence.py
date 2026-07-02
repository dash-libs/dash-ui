"""Unit tests for config persistence (no Spark required). Isolates HOME and
cwd per test via monkeypatch/tmp_path so nothing touches the real filesystem
outside the test sandbox."""
import os

import pytest


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    monkeypatch.delenv("DASHLIBS_CONFIG_DIR", raising=False)
    yield tmp_path


def test_get_config_dir_defaults_to_cwd(tmp_path, monkeypatch):
    from dashui.persistence import get_config_dir

    workdir = tmp_path / "notebook_dir"
    workdir.mkdir()
    monkeypatch.chdir(workdir)
    assert get_config_dir("dashtest") == str(workdir)


def test_get_config_dir_respects_env_var_override(tmp_path, monkeypatch):
    from dashui.persistence import get_config_dir

    override = tmp_path / "explicit_dir"
    monkeypatch.setenv("DASHLIBS_CONFIG_DIR", str(override))
    assert get_config_dir("dashtest") == str(override)


def test_set_config_dir_persists_across_calls(tmp_path):
    from dashui.persistence import get_config_dir, set_config_dir

    configured = tmp_path / "workspace_configs"
    set_config_dir("dashtest", str(configured))
    assert get_config_dir("dashtest") == str(configured)


def test_set_config_dir_wins_over_cwd_and_env_var(tmp_path, monkeypatch):
    from dashui.persistence import get_config_dir, set_config_dir

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DASHLIBS_CONFIG_DIR", str(tmp_path / "env_var_dir"))
    set_config_dir("dashtest", str(tmp_path / "explicit"))
    assert get_config_dir("dashtest") == str(tmp_path / "explicit")


def test_clear_config_dir_falls_back_to_cwd(tmp_path, monkeypatch):
    from dashui.persistence import clear_config_dir, get_config_dir, set_config_dir

    monkeypatch.chdir(tmp_path)
    set_config_dir("dashtest", str(tmp_path / "explicit"))
    clear_config_dir("dashtest")
    assert get_config_dir("dashtest") == str(tmp_path)


def test_clear_config_dir_is_a_noop_when_never_set():
    from dashui.persistence import clear_config_dir

    clear_config_dir("dashtest-never-configured")  # should not raise


def test_save_and_load_config_round_trip(tmp_path, monkeypatch):
    from dashui.persistence import load_config, save_config

    monkeypatch.chdir(tmp_path)
    path = save_config("dashtest", {"table": "main.bronze.customers", "mode": "append"})
    assert os.path.exists(path)
    assert load_config("dashtest") == {"table": "main.bronze.customers", "mode": "append"}


def test_load_config_returns_defaults_when_file_missing(tmp_path, monkeypatch):
    from dashui.persistence import load_config

    monkeypatch.chdir(tmp_path)
    assert load_config("dashtest-nonexistent", defaults={"mode": "append"}) == {"mode": "append"}


def test_load_config_merges_over_defaults(tmp_path, monkeypatch):
    from dashui.persistence import load_config, save_config

    monkeypatch.chdir(tmp_path)
    save_config("dashtest", {"mode": "overwrite"})
    result = load_config("dashtest", defaults={"mode": "append", "schema_evolution": True})
    assert result == {"mode": "overwrite", "schema_evolution": True}


def test_load_config_survives_corrupt_json(tmp_path, monkeypatch):
    from dashui.persistence import config_path, load_config

    monkeypatch.chdir(tmp_path)
    path = config_path("dashtest")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("{not valid json")
    assert load_config("dashtest", defaults={"ok": True}) == {"ok": True}


def test_different_libraries_and_names_use_separate_files(tmp_path, monkeypatch):
    from dashui.persistence import load_config, save_config

    monkeypatch.chdir(tmp_path)
    save_config("dashingest", {"a": 1}, name="source")
    save_config("dashingest", {"a": 2}, name="target")
    save_config("dashml", {"a": 3}, name="source")
    assert load_config("dashingest", name="source") == {"a": 1}
    assert load_config("dashingest", name="target") == {"a": 2}
    assert load_config("dashml", name="source") == {"a": 3}
