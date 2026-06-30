"""
DashUI — shared ipywidgets component library for the Dashlibs suite.
Import from here in any dash-* package instead of duplicating widget code.
"""
from dashui.components import (
    SourceSelector,
    action_button,
    card,
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
    BORDER,
    CARD,
    DANGER,
    FONT_MONO,
    FONT_SANS,
    MUTED,
    PRIMARY,
    SUCCESS,
    WARNING,
    accent,
)

__version__ = "0.1.2"
__all__ = [
    "SourceSelector",
    "action_button",
    "card",
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
    "BORDER",
    "CARD",
    "MUTED",
    "FONT_SANS",
    "FONT_MONO",
]
