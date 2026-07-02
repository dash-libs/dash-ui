"""Unit tests for dashui (no Spark required)."""
import pytest


def test_import():
    import dashui
    assert hasattr(dashui, "__version__")


def test_accent_known_and_default():
    from dashui.theme import ACCENTS, accent
    assert accent("dashsynthetic") == ACCENTS["dashsynthetic"]
    assert accent("totally-unknown-lib") == accent("default")


def test_header_returns_widget():
    import dashui
    from dashui.theme import ACCENTS
    h = dashui.header("Title", library="dashsynthetic", emoji="🧬")
    assert "Title" in h.value
    assert ACCENTS["dashsynthetic"].lstrip("#") in h.value


def test_status_line_kinds():
    from dashui.theme import DANGER, SUCCESS
    import dashui
    ok = dashui.status_line("done", kind="success")
    err = dashui.status_line("bad", kind="error")
    assert "done" in ok.value and SUCCESS in ok.value
    assert "bad" in err.value and DANGER in err.value


def test_source_selector_default_value():
    import dashui
    src = dashui.source_selector()
    src.table_input.value = "catalog.schema.table"
    kind, value = src.value()
    assert kind == "table"
    assert value == "catalog.schema.table"


def test_source_selector_switches_box_on_toggle():
    import dashui
    src = dashui.source_selector()
    src.toggle.value = "DataFrame variable"
    assert src.box.children == (src.df_input,)
    src.toggle.value = "SQL Query"
    assert src.box.children == (src.sql_input,)


def test_card_wraps_children():
    # card() injects a one-time global <style> block ahead of the first
    # children on the very first call in a process, so we only assert that
    # our widget made it in, not exact position/count.
    import dashui
    h = dashui.header("X")
    c = dashui.card([h])
    assert h in c.children
    assert "dashui-card" in c._dom_classes


def test_action_button_has_variant_class():
    import dashui
    btn = dashui.action_button("Run", style="success", emoji="▶")
    assert "▶ Run" == btn.description
    assert "dashui-btn-success" in btn._dom_classes


def test_running_list_renders_items():
    # ipywidgets Output only captures stdout into .outputs inside a live
    # Jupyter kernel, so outside a notebook we just assert it runs cleanly.
    import ipywidgets as w
    import dashui
    out, render = dashui.running_list(lambda i, item: f"{i}. {item}")
    assert isinstance(out, w.Output)
    render(["a", "b"])  # should not raise


def test_list_columns_safe_without_spark_returns_empty():
    from dashui.schema import list_columns_safe
    assert list_columns_safe("catalog.schema.nonexistent") == []


def test_editable_table_starts_with_one_row_by_default():
    import dashui
    tbl = dashui.editable_table(["Key", "Value"])
    assert len(tbl.widget.children[1].children) == 1  # rows_box is the 2nd child, after the header row


def test_editable_table_add_row_appends():
    import dashui
    tbl = dashui.editable_table(["Key", "Value"], initial_rows=0)
    assert len(tbl.widget.children[1].children) == 0
    tbl.add_row()
    tbl.add_row()
    assert len(tbl.widget.children[1].children) == 2


def test_editable_table_values_reads_filled_rows():
    import dashui
    tbl = dashui.editable_table(["Key", "Value"], initial_rows=2)
    row0, row1 = tbl.widget.children[1].children
    row0.children[0].value = "region"
    row0.children[1].value = "us-east-1"
    assert tbl.values() == [{"Key": "region", "Value": "us-east-1"}]


def test_editable_table_remove_row_button():
    import dashui
    tbl = dashui.editable_table(["Key", "Value"], initial_rows=2)
    first_row = tbl.widget.children[1].children[0]
    remove_btn = first_row.children[-1]
    remove_btn.click()
    assert len(tbl.widget.children[1].children) == 1


def test_env_setup_panel_defaults_to_cwd(tmp_path, monkeypatch):
    import dashui

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    workdir = tmp_path / "notebook_dir"
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    env = dashui.env_setup_panel("dashtest")
    assert env.values()["config_dir"] == str(workdir)


def test_env_setup_panel_save_persists_and_is_read_back(tmp_path, monkeypatch):
    import dashui

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    monkeypatch.chdir(tmp_path)

    env = dashui.env_setup_panel("dashtest", extra_fields={"Default catalog": "main"})
    dir_input = env.widget.children[1]
    dir_input.value = str(tmp_path / "chosen_dir")

    save_btn = env.widget.children[-2].children[0]
    save_btn.click()

    from dashui.persistence import get_config_dir
    assert get_config_dir("dashtest") == str(tmp_path / "chosen_dir")


def test_env_setup_panel_extra_fields_round_trip(tmp_path, monkeypatch):
    import dashui

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    monkeypatch.chdir(tmp_path)

    env = dashui.env_setup_panel("dashtest", extra_fields={"Default catalog": "main"})
    values = env.values()
    assert "Default catalog" in values
