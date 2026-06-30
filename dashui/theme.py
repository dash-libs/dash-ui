"""Shared color palette for Dashlibs notebook UIs — one accent per library."""
from __future__ import annotations

ACCENTS = {
    "dashdq": "#1B3A4B",
    "dashsynthetic": "#7B1FA2",
    "dashrelate": "#4527A0",
    "dashgov": "#00695C",
    "dashingest": "#EF6C00",
    "dashml": "#283593",
    "default": "#1B3A4B",
}

NEUTRAL = "#5C6673"
MUTED = "#9CA3AF"
BORDER = "#E5E7EB"
SUCCESS = "#43A047"
DANGER = "#C62828"
WARNING = "#F57C00"


def accent(library: str) -> str:
    """Look up the accent color for a Dashlibs package name (e.g. 'dashsynthetic')."""
    return ACCENTS.get(library, ACCENTS["default"])
