# -*- coding: utf-8 -*-
"""
Composants du Dashboard ZAN
"""

from .header import render_header
from .kpis import render_kpis
from .charts import (
    render_evolution_chart,
    render_repartition_chart,
    render_top_communes_chart,
    render_trajectory_chart,
)
from .filters import render_filters
from .tables import render_data_table

__all__ = [
    "render_header",
    "render_kpis",
    "render_evolution_chart",
    "render_repartition_chart",
    "render_top_communes_chart",
    "render_trajectory_chart",
    "render_filters",
    "render_data_table",
]

