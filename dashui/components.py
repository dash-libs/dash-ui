"""
Reusable ipywidgets building blocks shared across Dashlibs notebook UIs.
Works inside Databricks notebooks and plain Jupyter (both render ipywidgets).
"""
from __future__ import annotations
from dataclasses import dataclass

from dashui.theme import accent, BORDER, DANGER, MUTED, NEUTRAL, SUCCESS


def _require_widgets():
    try:
        import ipywidgets as w
        return w
    except ImportError:
        raise RuntimeError("ipywidgets required. Run: %pip install ipywidgets")


def html(text: str):
    w = _require_widgets()
    return w.HTML(text)


def header(title: str, library: str = "default", emoji: str = "", subtitle: str = ""):
    """Top banner used at the start of every launch() UI."""
    color = accent(library)
    sub = f"<div style='font-size:12px;color:{MUTED};margin-top:2px'>{subtitle}</div>" if subtitle else ""
    return html(
        f"<h2 style='color:{color};margin-bottom:0'>{emoji} {title}</h2>{sub}"
    )


def section(title: str):
    """Step/section divider, e.g. '<b>Step 1: Source data</b>'."""
    return html(f"<hr><b>{title}</b>")


def status_line(text: str, kind: str = "info"):
    """One-line colored status message: kind in success|error|warning|info."""
    color = {"success": SUCCESS, "error": DANGER, "warning": "#F57C00", "info": NEUTRAL}.get(kind, NEUTRAL)
    prefix = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(kind, "")
    return html(f"<span style='color:{color}'>{prefix} {text}</span>")


def card(children, padding: str = "16px"):
    """Bordered VBox wrapper used as the outer container for every launch() UI."""
    w = _require_widgets()
    return w.VBox(list(children), layout=w.Layout(
        padding=padding, border=f"1px solid {BORDER}", border_radius="8px",
    ))


@dataclass
class SourceSelector:
    """
    The UC Table / DataFrame variable / SQL Query picker used by every
    Dashlibs UI that reads from Databricks.

    Usage::
        src = source_selector()
        ui = card([src.toggle, src.box, ...])
        kind, value = src.value()
    """
    toggle: object
    box: object
    table_input: object
    df_input: object
    sql_input: object

    def value(self) -> tuple[str, str]:
        """Returns (kind, value) where kind is 'table' | 'dataframe' | 'sql'."""
        if self.toggle.value == "UC Table":
            return "table", self.table_input.value.strip()
        if self.toggle.value == "DataFrame variable":
            return "dataframe", self.df_input.value.strip()
        return "sql", self.sql_input.value.strip()

    def resolve_df(self):
        """Resolve the selected source to a Spark DataFrame (for direct use in core classes)."""
        kind, value = self.value()
        if kind == "dataframe":
            import IPython
            shell = IPython.get_ipython()
            df = shell.user_ns.get(value) if shell else None
            if df is None:
                raise ValueError(f"Variable '{value}' not found")
            return df
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()
        if kind == "table":
            return spark.table(value)
        return spark.sql(value)


def source_selector(label: str = "Source:") -> SourceSelector:
    w = _require_widgets()
    toggle = w.ToggleButtons(options=["UC Table", "DataFrame variable", "SQL Query"], description=label)
    table_input = w.Text(placeholder="catalog.schema.table", description="Table:")
    df_input = w.Text(placeholder="df", description="Variable:")
    sql_input = w.Textarea(placeholder="SELECT * FROM ...", description="SQL:", rows=3)
    box = w.VBox([table_input])

    def on_change(change):
        if change["new"] == "UC Table":
            box.children = [table_input]
        elif change["new"] == "DataFrame variable":
            box.children = [df_input]
        else:
            box.children = [sql_input]

    toggle.observe(on_change, names="value")
    return SourceSelector(toggle, box, table_input, df_input, sql_input)


def action_button(text: str, style: str = "primary", emoji: str = ""):
    w = _require_widgets()
    label = f"{emoji} {text}".strip()
    return w.Button(description=label, button_style=style, layout=w.Layout(height="36px"))


def output_panel():
    """Standard scrollable output area for run/profile results and errors."""
    w = _require_widgets()
    return w.Output()


def running_list(formatter):
    """
    A live-updating numbered list display, the pattern used for 'added entities'
    / 'added relationships' style accumulators.

    Usage::
        items = []
        out, render = running_list(lambda i, item: f"{i}. {item['name']}")
        items.append({"name": "Customer"})
        render(items)
    """
    w = _require_widgets()
    out = w.Output()

    def render(items: list):
        with out:
            out.clear_output()
            for i, item in enumerate(items, 1):
                print(formatter(i, item))

    return out, render
