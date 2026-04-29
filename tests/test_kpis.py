import pandas as pd

from src.analytics.kpis import build_weekly_totals, calc_ticket_medio, calc_wow


def test_calc_ticket_medio() -> None:
    assert calc_ticket_medio(100, 4) == 25
    assert calc_ticket_medio(100, 0) == 0


def test_calc_wow() -> None:
    assert round(calc_wow(120, 100), 2) == 20.0
    assert calc_wow(100, 0) == 0.0


def test_build_weekly_totals() -> None:
    df = pd.DataFrame([
        {"anio_iso": 2026, "semana_iso": 1, "ventas_totales_bruto": 100, "num_pedidos": 5},
        {"anio_iso": 2026, "semana_iso": 1, "ventas_totales_bruto": 30, "num_pedidos": 2},
    ])
    out = build_weekly_totals(df)
    assert float(out.iloc[0]["ventas_totales_bruto"]) == 130
    assert int(out.iloc[0]["num_pedidos"]) == 7
