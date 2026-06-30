# Databricks notebook source
# MAGIC %md
# MAGIC # dash-ui — Shared UI Components
# MAGIC
# MAGIC Reusable ipywidgets building blocks for any Dashlibs notebook UI.
# MAGIC
# MAGIC **Install:**

# COMMAND ----------

# MAGIC %pip install dash-uis

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import dashui

header = dashui.header("Example", library="dashsynthetic", emoji="🧬")
src = dashui.source_selector()
btn = dashui.action_button("Run", style="success", emoji="▶")
out = dashui.output_panel()

ui = dashui.card([header, src.toggle, src.box, btn, out])
ui

# COMMAND ----------
# MAGIC %md
# MAGIC ## Python API (optional — for automation)
# MAGIC
# MAGIC ```python
# MAGIC import dashui
# MAGIC # See docs/api/ for full API reference
# MAGIC ```
