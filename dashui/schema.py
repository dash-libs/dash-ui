"""Unity Catalog schema introspection helpers shared across Dashlibs UIs."""
from __future__ import annotations


def list_columns(table: str) -> list[str]:
    """Return column names for a UC table, without loading any data."""
    from pyspark.sql import SparkSession
    spark = SparkSession.getActiveSession()
    return [f.name for f in spark.table(table).schema.fields]


def list_columns_safe(table: str) -> list[str]:
    """Like list_columns, but returns [] instead of raising — for UI dropdowns."""
    try:
        return list_columns(table)
    except Exception:
        return []
