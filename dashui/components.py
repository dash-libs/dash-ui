"""
Reusable ipywidgets building blocks shared across Dashlibs notebook UIs.
Visually modeled on Databricks' own product UI (Inter, Lava-red primary
reserved for primary actions, small-radius neutral cards, dense tabular
forms) — translated into the CSS ipywidgets can actually render inside a
notebook output cell. See theme.py's docstring for sourcing notes.
"""
from __future__ import annotations
from dataclasses import dataclass

from dashui.theme import (
    ACCENT_BG,
    ACCENT_FG,
    BORDER,
    BORDER_STRONG,
    CARD,
    DANGER,
    FONT_IMPORT_URL,
    FONT_MONO,
    FONT_SANS,
    FONT_SIZE_BASE,
    MUTED,
    MUTED_FOREGROUND,
    PRIMARY,
    PRIMARY_HOVER,
    RADIUS_LG,
    RADIUS_MD,
    RADIUS_SM,
    SHADOW_SM,
    SUCCESS,
    WARNING,
    accent,
)

_STYLE_INJECTED = False

_BUTTON_VARIANTS = {
    # button_style name -> (background, text color, hover background, border)
    "primary": (PRIMARY, "#FFFFFF", PRIMARY_HOVER, PRIMARY),
    "success": (SUCCESS, "#FFFFFF", "#256628", SUCCESS),
    "warning": (WARNING, "#FFFFFF", "#8F5600", WARNING),
    "danger": (DANGER, "#FFFFFF", "#A02020", DANGER),
    "info": (CARD, "#1B3139", MUTED, BORDER_STRONG),
    "": (CARD, "#1B3139", MUTED, BORDER_STRONG),
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
    """The shared <style> block (fonts, card shell, inputs, tabs, table, button variants)."""
    btn_css = "\n".join(
        f".dashui-btn-{name or 'default'}.widget-button {{ "
        f"background:{bg} !important; color:{fg} !important; "
        f"border:1px solid {border} !important; "
        f"border-radius:{RADIUS_MD} !important; font-weight:500 !important; font-size:{FONT_SIZE_BASE} !important; "
        f"font-family:{FONT_SANS} !important; height:32px !important; box-shadow:none !important; "
        f"transition:background-color .12s ease, border-color .12s ease; }}\n"
        f".dashui-btn-{name or 'default'}.widget-button:hover {{ background:{hover} !important; border-color:{hover} !important; }}"
        for name, (bg, fg, hover, border) in _BUTTON_VARIANTS.items()
        if name
    )
    return html(f"""
<style>
@import url('{FONT_IMPORT_URL}');

.dashui-root, .dashui-root * {{ font-family: {FONT_SANS} !important; font-size: {FONT_SIZE_BASE}; color: #1B3139; }}

/* ── Card shell ─────────────────────────────────────────────────────── */
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
    font-size: {FONT_SIZE_BASE};
}}

/* ── Form inputs — flat, bordered, small radius, Lava focus ring ──────── */
.dashui-root input[type="text"], .dashui-root input[type="password"],
.dashui-root input[type="number"], .dashui-root textarea, .dashui-root select {{
    border: 1px solid {BORDER_STRONG} !important;
    border-radius: {RADIUS_SM} !important;
    background: {CARD} !important;
    font-size: {FONT_SIZE_BASE} !important;
    padding: 4px 8px !important;
    box-shadow: none !important;
    transition: border-color .12s ease, box-shadow .12s ease;
}}
.dashui-root input[type="text"]:focus, .dashui-root input[type="password"]:focus,
.dashui-root input[type="number"]:focus, .dashui-root textarea:focus, .dashui-root select:focus {{
    border-color: {PRIMARY} !important;
    box-shadow: 0 0 0 2px {ACCENT_BG} !important;
    outline: none !important;
}}
.dashui-root input[type="checkbox"] {{ accent-color: {PRIMARY}; }}
.dashui-root .widget-label {{ font-size: {FONT_SIZE_BASE} !important; color: #1B3139 !important; font-weight: 500; }}

/* ── ToggleButtons — segmented control, filled-when-selected ─────────── */
.dashui-root .widget-toggle-buttons .widget-toggle-button {{
    border: 1px solid {BORDER_STRONG} !important;
    background: {CARD} !important;
    color: #1B3139 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    font-size: {FONT_SIZE_BASE} !important;
    font-weight: 500 !important;
}}
.dashui-root .widget-toggle-buttons .widget-toggle-button:first-child {{ border-radius: {RADIUS_SM} 0 0 {RADIUS_SM} !important; }}
.dashui-root .widget-toggle-buttons .widget-toggle-button:last-child {{ border-radius: 0 {RADIUS_SM} {RADIUS_SM} 0 !important; }}
.dashui-root .widget-toggle-buttons .mod-active {{
    background: {ACCENT_BG} !important;
    border-color: {PRIMARY} !important;
    color: {ACCENT_FG} !important;
    font-weight: 600 !important;
}}

/* ── Tabs — underline style, matching the Databricks workspace nav ────── */
.dashui-root .widget-tab > .p-TabBar, .dashui-root .widget-tab > .lm-TabBar {{
    border-bottom: 1px solid {BORDER} !important;
}}
.dashui-root .p-TabBar-tab, .dashui-root .lm-TabBar-tab {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: {MUTED_FOREGROUND} !important;
    font-size: {FONT_SIZE_BASE} !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
}}
.dashui-root .p-TabBar-tab.p-mod-current, .dashui-root .lm-TabBar-tab.lm-mod-current {{
    color: {PRIMARY} !important;
    border-bottom: 2px solid {PRIMARY} !important;
    font-weight: 600 !important;
}}
.dashui-root .widget-tab-contents {{ border: none !important; padding-top: 12px !important; }}

/* ── Editable table — Databricks "parameters" table pattern ───────────── */
.dashui-table {{ border: 1px solid {BORDER}; border-radius: {RADIUS_MD}; overflow: hidden; }}
.dashui-table-row {{
    border-bottom: 1px solid {BORDER};
    padding: 4px 8px;
    align-items: center;
}}
.dashui-table-row:last-child {{ border-bottom: none; }}
.dashui-table-row:hover {{ background: {MUTED}; }}
.dashui-table-header {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: {MUTED_FOREGROUND};
    background: {MUTED};
    padding: 6px 8px;
}}
.dashui-mono {{ font-family: {FONT_MONO} !important; font-size: 12px !important; }}

{btn_css}
</style>
""")


def header(title: str, library: str = "default", emoji: str = "", subtitle: str = ""):
    """Top banner used at the start of every launch() UI. `emoji` is kept for
    API compatibility but not used by any dash-* package — Databricks' own
    page headers are plain text, no decorative glyph."""
    color = accent(library)
    prefix = f"{emoji} " if emoji else ""
    sub = (
        f"<div style='font-size:12px;color:{MUTED_FOREGROUND};margin-top:2px;"
        f"font-family:{FONT_SANS}'>{subtitle}</div>"
    ) if subtitle else ""
    return html(
        f"<h2 style='color:{color};margin-bottom:0;font-weight:700;"
        f"letter-spacing:-0.01em;font-family:{FONT_SANS}'>{prefix}{title}</h2>{sub}"
    )


def section(title: str):
    """Step/section divider, styled like the datapal-access card label convention."""
    return html(f"<div class='dashui-section'>{title}</div>")


def status_line(text: str, kind: str = "info"):
    """One-line status message: kind in success|error|warning|info. A small
    solid dot carries the color instead of a colorful emoji — closer to how
    Databricks' own job/cluster status indicators read."""
    color = {"success": SUCCESS, "error": DANGER, "warning": WARNING, "info": MUTED_FOREGROUND}.get(kind, MUTED_FOREGROUND)
    return html(
        f"<span style='font-family:{FONT_SANS};color:#1B3139'>"
        f"<span style='display:inline-block;width:6px;height:6px;border-radius:50%;"
        f"background:{color};margin-right:7px'></span>{text}</span>"
    )


def card(children, padding: str = "16px"):
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
    """style in primary|success|warning|danger|info — matches the Databricks
    button variants. `emoji` is kept for API compatibility but not used by
    any dash-* package — Databricks buttons are plain text, no glyph."""
    w = _require_widgets()
    label = f"{emoji} {text}".strip()
    btn = w.Button(description=label, layout=w.Layout(height="32px", padding="0 14px", width="auto"))
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


@dataclass
class EditableTable:
    """
    An add/remove-row key-value grid — the pattern Databricks itself uses for
    job parameters, cluster tags, and environment variables, instead of a
    single free-text "key=value, key=value" field.

    Usage::
        tbl = editable_table(["Key", "Value"], placeholders={"Key": "AWS_REGION"})
        ui = card([tbl.widget, ...])
        rows = tbl.values()  # [{"Key": "AWS_REGION", "Value": "us-east-1"}, ...]
    """
    widget: object
    add_row: object   # callable(b=None) -> None, wired as a Button.on_click handler too
    values: object     # callable() -> list[dict[str, str]]


def editable_table(columns: list[str], placeholders: dict[str, str] | None = None, initial_rows: int = 1) -> EditableTable:
    w = _require_widgets()
    placeholders = placeholders or {}
    row_entries: list[tuple[object, dict]] = []  # (row_box, {col: Text widget})

    header_row = w.HBox(
        [w.HTML(f"<div class='dashui-table-header'>{col}</div>") for col in columns] + [w.HTML("", layout=w.Layout(width="32px"))]
    )
    rows_box = w.VBox([])

    def _make_row():
        cells = {col: w.Text(placeholder=placeholders.get(col, ""), layout=w.Layout(width="auto", flex="1")) for col in columns}
        remove_btn = w.Button(description="✕", layout=w.Layout(width="32px", height="28px"), tooltip="Remove row")
        remove_btn.add_class("dashui-btn-info")
        row_box = w.HBox([cells[c] for c in columns] + [remove_btn])
        row_box.add_class("dashui-table-row")

        def on_remove(_b):
            row_entries[:] = [(rb, c) for rb, c in row_entries if rb is not row_box]
            rows_box.children = tuple(rb for rb, _ in row_entries)

        remove_btn.on_click(on_remove)
        return row_box, cells

    def add_row(_b=None):
        row_box, cells = _make_row()
        row_entries.append((row_box, cells))
        rows_box.children = tuple(rb for rb, _ in row_entries)

    for _ in range(initial_rows):
        add_row()

    add_btn = action_button("Add row", style="info", emoji="＋")
    add_btn.on_click(add_row)

    def values() -> list[dict]:
        return [
            {col: cells[col].value.strip() for col in columns}
            for _, cells in row_entries
            if any(cells[col].value.strip() for col in columns)
        ]

    table = w.VBox([header_row, rows_box, add_btn])
    table.add_class("dashui-table")
    return EditableTable(widget=table, add_row=add_row, values=values)


def env_setup_panel(library: str, extra_fields: dict | None = None):
    """
    A ready-to-embed "Environment Setup" panel: where should this package's
    configs live? Defaults to the notebook's current working directory;
    Save remembers a different directory (e.g. a Workspace path or Volume)
    for every future session, across notebooks.

    `extra_fields` is `{label: placeholder}` for any library-specific
    defaults (e.g. {"Default catalog": "main"}) — saved alongside the
    directory choice and available via the returned `values()`.

    Usage::
        env = dashui.env_setup_panel("dashingest", extra_fields={"Default catalog": "main"})
        ui = card([..., env.widget, ...])
        settings = env.values()  # {"config_dir": ..., "Default catalog": ...}
    """
    from dashui.persistence import get_config_dir, load_config, save_config, set_config_dir

    w = _require_widgets()
    extra_fields = extra_fields or {}
    saved = load_config(library, name="env")

    dir_input = w.Text(
        description="Config directory:",
        value=saved.get("config_dir", get_config_dir(library)),
        placeholder=get_config_dir(library),
        layout=w.Layout(width="420px"),
    )
    extra_inputs = {
        label: w.Text(description=f"{label}:", value=saved.get(label, ""), placeholder=placeholder)
        for label, placeholder in extra_fields.items()
    }

    save_btn = action_button("Save", style="primary")
    reload_btn = action_button("Reload", style="info")
    status = html(f"<span style='font-size:12px;color:{MUTED_FOREGROUND}'>Currently using: <code>{get_config_dir(library)}</code></span>")

    def _collect() -> dict:
        return {"config_dir": dir_input.value.strip() or get_config_dir(library),
                **{label: field.value for label, field in extra_inputs.items()}}

    def _on_save(_b):
        config = _collect()
        set_config_dir(library, config["config_dir"])
        path = save_config(library, config, name="env")
        status.value = f"<span style='font-size:12px;color:{SUCCESS}'>Saved — settings will be read from <code>{path}</code> in future sessions.</span>"

    def _on_reload(_b):
        current = load_config(library, name="env")
        dir_input.value = current.get("config_dir", get_config_dir(library))
        for label, field in extra_inputs.items():
            field.value = current.get(label, "")
        status.value = f"<span style='font-size:12px;color:{MUTED_FOREGROUND}'>Reloaded from <code>{config_path_display(library)}</code>.</span>"

    save_btn.on_click(_on_save)
    reload_btn.on_click(_on_reload)

    panel = w.VBox([
        html(
            f"<div style='font-size:12px;color:{MUTED_FOREGROUND};margin-bottom:4px'>"
            "Where should this package's configs be read/written? Leave as-is to use "
            "the notebook's current working directory — nothing here is required."
            "</div>"
        ),
        dir_input,
        *extra_inputs.values(),
        w.HBox([save_btn, reload_btn]),
        status,
    ])
    return EnvSetupPanel(widget=panel, values=_collect)


def config_path_display(library: str) -> str:
    from dashui.persistence import config_path
    return config_path(library, name="env")


@dataclass
class EnvSetupPanel:
    widget: object
    values: object  # callable() -> dict
