"""
Reusable ipywidgets building blocks shared across Dashlibs notebook UIs.
Visually modeled on the datapal-access Databricks App (IBM Plex Sans, teal
primary, rounded-lg cards with a soft shadow) — translated into the CSS
ipywidgets can actually render inside a notebook output cell.
"""
from __future__ import annotations
from dataclasses import dataclass

from dashui.theme import (
    BORDER,
    CARD,
    DANGER,
    FONT_IMPORT_URL,
    FONT_SANS,
    MUTED,
    MUTED_FOREGROUND,
    PRIMARY,
    RADIUS_LG,
    RADIUS_MD,
    SHADOW_SM,
    SUCCESS,
    WARNING,
    accent,
)

_STYLE_INJECTED = False

_BUTTON_VARIANTS = {
    # button_style name -> (background, text color, hover background)
    "primary": (PRIMARY, "#FFFFFF", "#23867B"),
    "success": (SUCCESS, "#FFFFFF", "#228758"),
    "warning": (WARNING, "#FFFFFF", "#D88A00"),
    "danger": (DANGER, "#FFFFFF", "#BD2222"),
    "info": (MUTED, "#131720", "#E4E7EB"),
    "": (MUTED, "#131720", "#E4E7EB"),
}


def _require_widgets():
    try:
        import ipywidgets as w
        return w
    except ImportError:
        raise RuntimeError("ipywidgets required. Run: %pip install ipywidgets")


def html(text: str):
    w = _require_widgets()
    return w.HTML(text)


def _global_style():
    """The shared <style> block (fonts, card shell, button variants, output panel)."""
    btn_css = "\n".join(
        f".dashui-btn-{name or 'default'}.widget-button {{ "
        f"background:{bg} !important; color:{fg} !important; border:none !important; "
        f"border-radius:{RADIUS_MD} !important; font-weight:600 !important; "
        f"font-family:{FONT_SANS} !important; transition:background-color .15s ease; }}\n"
        f".dashui-btn-{name or 'default'}.widget-button:hover {{ background:{hover} !important; }}"
        for name, (bg, fg, hover) in _BUTTON_VARIANTS.items()
        if name
    )
    return html(f"""
<style>
@import url('{FONT_IMPORT_URL}');
.dashui-root, .dashui-root * {{ font-family: {FONT_SANS} !important; }}
.dashui-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_LG};
    box-shadow: {SHADOW_SM};
}}
.dashui-section {{
    color: {MUTED_FOREGROUND};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 6px;
    margin-top: 4px;
}}
.dashui-output {{
    background: {MUTED};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_MD};
}}
{btn_css}
</style>
""")


def header(title: str, library: str = "default", emoji: str = "", subtitle: str = ""):
    """Top banner used at the start of every launch() UI."""
    color = accent(library)
    sub = (
        f"<div style='font-size:12px;color:{MUTED_FOREGROUND};margin-top:2px;"
        f"font-family:{FONT_SANS}'>{subtitle}</div>"
    ) if subtitle else ""
    return html(
        f"<h2 style='color:{color};margin-bottom:0;font-weight:700;"
        f"letter-spacing:-0.01em;font-family:{FONT_SANS}'>{emoji} {title}</h2>{sub}"
    )


def section(title: str):
    """Step/section divider, styled like the datapal-access card label convention."""
    return html(f"<div class='dashui-section'>{title}</div>")


def status_line(text: str, kind: str = "info"):
    """One-line colored status message: kind in success|error|warning|info."""
    color = {"success": SUCCESS, "error": DANGER, "warning": WARNING, "info": MUTED_FOREGROUND}.get(kind, MUTED_FOREGROUND)
    prefix = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(kind, "")
    return html(f"<span style='color:{color};font-family:{FONT_SANS}'>{prefix} {text}</span>")


def card(children, padding: str = "20px"):
    """Bordered, shadowed VBox container — the outer shell for every launch() UI."""
    w = _require_widgets()
    global _STYLE_INJECTED
    body = [_global_style(), *children] if not _STYLE_INJECTED else list(children)
    _STYLE_INJECTED = True
    box = w.VBox(body, layout=w.Layout(padding=padding))
    box.add_class("dashui-card")
    box.add_class("dashui-root")
    return box


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
    """style in primary|success|warning|danger|info — matches the datapal-access button variants."""
    w = _require_widgets()
    label = f"{emoji} {text}".strip()
    btn = w.Button(description=label, layout=w.Layout(height="40px", padding="0 16px"))
    btn.add_class(f"dashui-btn-{style or 'default'}")
    return btn


def output_panel():
    """Standard scrollable output area for run/profile results and errors."""
    w = _require_widgets()
    out = w.Output(layout=w.Layout(padding="12px"))
    out.add_class("dashui-output")
    return out


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
    out = w.Output(layout=w.Layout(padding="8px 12px"))
    out.add_class("dashui-output")

    def render(items: list):
        with out:
            out.clear_output()
            for i, item in enumerate(items, 1):
                print(formatter(i, item))

    return out, render
