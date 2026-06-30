"""Unit tests for dashui (no Spark required)."""
import pytest


def test_import():
    import dashui
    assert hasattr(dashui, "__version__")


def test_accent_known_and_default():
    from dashui.theme import accent
    assert accent("dashsynthetic") == "#7B1FA2"
    assert accent("totally-unknown-lib") == accent("default")


def test_header_returns_widget():
    import dashui
    h = dashui.header("Title", library="dashsynthetic", emoji="🧬")
    assert "Title" in h.value
    assert "7B1FA2" in h.value


def test_status_line_kinds():
    import dashui
    ok = dashui.status_line("done", kind="success")
    err = dashui.status_line("bad", kind="error")
    assert "✅" in ok.value
    assert "❌" in err.value


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
