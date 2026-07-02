"""
DashUI — shared ipywidgets component library for the Dashlibs suite.
Import from here in any dash-* package instead of duplicating widget code.
"""
from dashui.components import (
    EditableTable,
    SourceSelector,
    action_button,
    card,
    editable_table,
    header,
    html,
    output_panel,
    running_list,
    section,
    source_selector,
    status_line,
)
from dashui.schema import list_columns, list_columns_safe
from dashui.theme import (
    ACCENT_BG,
    ACCENT_FG,
    BORDER,
    BORDER_STRONG,
    CARD,
    DANGER,
    FONT_MONO,
    FONT_SANS,
    INFO,
    MUTED,
    PRIMARY,
    SUCCESS,
    WARNING,
    accent,
)

__version__ = "0.2.1"
__all__ = [
    "SourceSelector",
    "EditableTable",
    "action_button",
    "card",
    "editable_table",
    "header",
    "html",
    "output_panel",
    "running_list",
    "section",
    "source_selector",
    "status_line",
    "list_columns",
    "list_columns_safe",
    "accent",
    "PRIMARY",
    "SUCCESS",
    "DANGER",
    "WARNING",
    "INFO",
    "BORDER",
    "BORDER_STRONG",
    "CARD",
    "MUTED",
    "ACCENT_BG",
    "ACCENT_FG",
    "FONT_SANS",
    "FONT_MONO",
]
