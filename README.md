# DashUI — Databricks Library

[![CI](https://github.com/dash-libs/dash-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/dash-libs/dash-ui/actions)
[![PyPI](https://img.shields.io/pypi/v/dash-uis)](https://pypi.org/project/dash-uis/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Part of the **[Dashlibs](https://github.com/dash-libs)** suite — Databricks libraries built for business users.

Shared `ipywidgets` components so every `dash-*` library looks and behaves the
same way inside a Databricks (or plain Jupyter) notebook: headers, the
UC Table / DataFrame / SQL source picker, output panels, status lines, and
schema introspection helpers — styled to match the team's
[datapal-access](https://github.com/dash-libs) Databricks App design system
(IBM Plex Sans, a teal primary, `rounded-lg` cards with a soft shadow)
instead of default ipywidgets styling.

## What it looks like

![DashUI components — header, source picker, buttons, status lines, output panel](https://raw.githubusercontent.com/dash-libs/dash-ui/main/docs/screenshots/components_preview.png)

*The top card is `dashsynthetic`'s "Single Table" tab, built entirely out of `dashui` components.*

## Installation

```bash
%pip install dash-uis
```

> Note: the PyPI distribution is named `dash-uis` (the name `dash-ui` was
> already taken by an unrelated package). The importable module is still `dashui`.

## Quick Start

```python
import dashui
from IPython.display import display

src = dashui.source_selector()
run_btn = dashui.action_button("Run", style="success", emoji="▶")
out = dashui.output_panel()

def on_run(b):
    with out:
        out.clear_output()
        kind, value = src.value()
        print(f"✅ Source: {kind} = {value!r}")

run_btn.on_click(on_run)

ui = dashui.card([
    dashui.header("My Library", library="dashsynthetic", emoji="🧬"),
    dashui.section("Step 1: Source data"),
    src.toggle, src.box,
    run_btn, out,
])
display(ui)
```

## Components

### `header(title, library="default", emoji="", subtitle="")`
The banner at the top of every `launch()` UI. Color comes from a per-library accent
(`dashsynthetic` is purple, `dashobserve` is red, etc. — see `dashui.theme.ACCENTS`).

```python
dashui.header("DashObserve — Data Observability", library="dashobserve", emoji="👁️")
```

### `section(title)`
A small uppercase step divider with a bottom border, used to break a form into steps
("Step 1: Source data", "Step 2: Generation settings", ...).

```python
dashui.section("Step 2: Generation settings")
```

### `source_selector(label="Source:")`
The UC Table / DataFrame variable / SQL Query picker used by every Dashlibs UI that
reads from Databricks. Returns a `SourceSelector` with `.toggle`, `.box` (swap-on-select
widgets) and helpers to resolve the chosen source.

```python
src = dashui.source_selector()
ui = dashui.card([src.toggle, src.box])

kind, value = src.value()   # ("table", "catalog.schema.customers")
df = src.resolve_df()       # resolves straight to a Spark DataFrame
```

### `action_button(text, style="primary", emoji="")`
A styled button matching the datapal-access button variants. `style` is one of
`primary | success | warning | danger | info`.

```python
run_btn = dashui.action_button("Generate Synthetic Data", style="success", emoji="▶")
```

### `status_line(text, kind="info")`
A one-line colored status message. `kind` is one of `success | error | warning | info`.

```python
dashui.status_line("Row count 9,842 within expected bounds", kind="success")
dashui.status_line("Schema changed — added: discount_code", kind="warning")
```

### `output_panel()`
The standard scrollable result/error area used under every action button — an
`ipywidgets.Output` pre-styled with a muted background and rounded border.

```python
out = dashui.output_panel()
with out:
    print("✅ Done")
```

### `running_list(formatter)`
A live-updating numbered list for "added items" accumulators (tables, relationships,
monitors, ...). Returns `(output_widget, render_fn)`.

```python
items = []
out, render = dashui.running_list(lambda i, item: f"{i}. {item['name']}")
items.append({"name": "Customer"})
render(items)
```

### `card(children, padding="20px")`
The bordered, shadowed container every `launch()` UI is wrapped in. Injects the shared
`<style>` block (fonts, button variants, card shell) once per notebook kernel.

```python
ui = dashui.card([header, section_title, src.toggle, src.box, run_btn, out])
display(ui)
```

### `list_columns(table)` / `list_columns_safe(table)`
UC table column introspection — `list_columns_safe` returns `[]` instead of raising,
which is what you want when populating a dropdown in a UI callback.

```python
cols = dashui.list_columns_safe("catalog.schema.customers")
```

### Design tokens
The raw palette is also exported for building fully custom widgets that still match
the system: `dashui.PRIMARY`, `dashui.SUCCESS`, `dashui.DANGER`, `dashui.WARNING`,
`dashui.BORDER`, `dashui.CARD`, `dashui.MUTED`, `dashui.FONT_SANS`, `dashui.FONT_MONO`.

## Part of Dashlibs

| Library | Purpose |
|---|---|
| dash-dq | Data Quality |
| dash-synthetic | Synthetic Data Generation |
| dash-observe | Data Observability (freshness, volume, schema) |
| dash-ml | ML Model Monitoring |
| dash-ingest | Data Ingestion |
| dash-gov | Data Governance |
| dash-relate | Ontology & Lineage for AI |
| dash-ui | Shared UI components (PyPI: `dash-uis`) |

## License

Apache 2.0
