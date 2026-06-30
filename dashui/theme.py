"""
Shared design tokens for Dashlibs notebook UIs.

The palette below is lifted from the datapal-access Databricks App
(React + Tailwind + shadcn/ui) so every dash-* notebook UI shares the same
look and feel as the team's flagship web app, not a default ipywidgets theme.
"""
from __future__ import annotations

# ── Per-library accent (used for headers / primary actions) ───────────────
ACCENTS = {
    "dashdq": "#1B3A4B",
    "dashsynthetic": "#7B1FA2",
    "dashrelate": "#4527A0",
    "dashgov": "#00695C",
    "dashingest": "#EF6C00",
    "dashml": "#283593",
    "dashobserve": "#B71C1C",
    "default": "#2A9D90",
}

# ── Neutral design system (datapal-access tokens) ──────────────────────────
BACKGROUND = "#F9FAFB"
FOREGROUND = "#131720"
CARD = "#FFFFFF"
BORDER = "#DAE0E7"
MUTED = "#F0F2F4"
MUTED_FOREGROUND = "#6A7181"
ACCENT_BG = "#E2F3F1"
ACCENT_FG = "#1B655C"

PRIMARY = "#2A9D90"
PRIMARY_FOREGROUND = "#FFFFFF"
SUCCESS = "#29A36A"
DANGER = "#DC2828"
WARNING = "#F59F0A"

RADIUS_LG = "8px"
RADIUS_MD = "6px"
RADIUS_SM = "4px"
SHADOW_SM = "0 1px 2px 0 rgba(0,0,0,0.05)"
SHADOW_MD = "0 2px 8px 0 rgba(0,0,0,0.08)"

FONT_SANS = "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_MONO = "'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace"

FONT_IMPORT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
)

# Backwards-compatible aliases (older callers imported these names directly)
NEUTRAL = MUTED_FOREGROUND


def accent(library: str) -> str:
    """Look up the accent color for a Dashlibs package name (e.g. 'dashsynthetic')."""
    return ACCENTS.get(library, ACCENTS["default"])
