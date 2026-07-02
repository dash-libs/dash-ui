"""
Shared design tokens for Dashlibs notebook UIs.

Previously modeled on the datapal-access Databricks App (Tailwind/shadcn).
Repointed to Databricks' own product design language instead — dense,
neutral, small-radius, table-heavy, with Databricks' signature "Lava"
red-orange reserved for primary actions rather than spread across the UI.
Source: Databricks' public brand identity (Lava #FF3621, navy #1B3139) plus
the visual conventions of the actual workspace product (Jobs/Clusters/
Catalog Explorer config screens — compact forms, tabbed sections, editable
parameter tables, 4-6px radii, thin light-gray borders). Not a pixel-exact
extraction the way datapal-access was (no live workspace to sample from in
this environment) — if you have reference screenshots to match more
precisely, bring them and these tokens should be the first thing revisited.
"""
from __future__ import annotations

# ── Per-library accent (used for headers only — primary actions always use
# the single Databricks Lava PRIMARY color, not a per-library color) ───────
ACCENTS = {
    "dashdq": "#1B3139",
    "dashsynthetic": "#5A3E85",
    "dashontology": "#3B4F7A",
    "dashgov": "#1B6B5C",
    "dashingest": "#B35900",
    "dashml": "#2D4A8A",
    "dashobserve": "#8A2E2E",
    "default": "#1B3139",
}

# ── Neutral design system (Databricks product UI conventions) ─────────────
BACKGROUND = "#F7F8F9"
FOREGROUND = "#1B3139"          # Databricks navy — primary text
CARD = "#FFFFFF"
BORDER = "#DCE0E2"
BORDER_STRONG = "#C7CCD1"
MUTED = "#F3F4F5"
MUTED_FOREGROUND = "#5A6872"
ACCENT_BG = "#FFF1EC"           # tint of Lava, for selected/hover states
ACCENT_FG = "#B33B1E"

PRIMARY = "#FF3621"             # Databricks "Lava" — reserved for primary actions
PRIMARY_HOVER = "#E62E1B"
PRIMARY_FOREGROUND = "#FFFFFF"
SUCCESS = "#2E7D32"
DANGER = "#C62828"
WARNING = "#B36B00"
INFO = "#0E6BA8"

RADIUS_LG = "6px"
RADIUS_MD = "4px"
RADIUS_SM = "3px"
SHADOW_SM = "0 1px 2px 0 rgba(27,49,57,0.06)"
SHADOW_MD = "0 2px 6px 0 rgba(27,49,57,0.10)"

FONT_SANS = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_MONO = "'Roboto Mono', 'SFMono-Regular', Consolas, monospace"

FONT_IMPORT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap"
)

# Base font size for the dense, product-like feel (vs. a marketing-site 16px)
FONT_SIZE_BASE = "13px"

# Backwards-compatible aliases (older callers imported these names directly)
NEUTRAL = MUTED_FOREGROUND


def accent(library: str) -> str:
    """Look up the accent color for a Dashlibs package name (e.g. 'dashsynthetic')."""
    return ACCENTS.get(library, ACCENTS["default"])
