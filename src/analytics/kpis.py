from __future__ import annotations

import pandas as pd


def calc_ticket_medio(ventas_totales: float, num_pedidos: int) -> float:
    return (ventas_totales / num_pedidos) if num_pedidos else 0.0


def calc_wow(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def build_weekly_totals(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["anio_iso", "semana_iso"], as_index=False)[["ventas_totales_bruto", "num_pedidos"]]
        .sum()
        .sort_values(["anio_iso", "semana_iso"])
    )
    return grouped
