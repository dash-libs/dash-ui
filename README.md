# DashUI — Databricks Library

[![CI](https://github.com/dash-libs/dash-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/dash-libs/dash-ui/actions)
[![PyPI](https://img.shields.io/pypi/v/dash-ui)](https://pypi.org/project/dash-ui/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Part of the **[Dashlibs](https://github.com/dash-libs)** suite — Databricks libraries built for business users.

Shared `ipywidgets` components so every `dash-*` library looks and behaves the
same way inside a Databricks (or plain Jupyter) notebook: headers, the
UC Table / DataFrame / SQL source picker, output panels, status lines, and
schema introspection helpers.

## Installation

```bash
%pip install dash-ui
```

## Usage

```python
import dashui

header = dashui.header("My Library", library="dashsynthetic", emoji="🧬")
src = dashui.source_selector()
btn = dashui.action_button("Run", style="success", emoji="▶")
out = dashui.output_panel()

ui = dashui.card([header, src.toggle, src.box, btn, out])
```

```python
kind, value = src.value()        # ("table", "catalog.schema.customers")
df = src.resolve_df()            # resolves to a Spark DataFrame
cols = dashui.list_columns_safe("catalog.schema.customers")
```

## Part of Dashlibs

| Library | Purpose |
|---|---|
| dash-dq | Data Quality |
| dash-synthetic | Synthetic Data Generation |
| dash-ml | ML Model Monitoring |
| dash-ingest | Data Ingestion |
| dash-gov | Data Governance |
| dash-relate | Ontology & Lineage for AI |
| dash-ui | Shared UI components |

## License

Apache 2.0
