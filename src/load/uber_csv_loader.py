from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class UberLoadBundle:
    sales_over_time: pd.DataFrame
    leaderboard_items: pd.DataFrame
    sales_hourly: pd.DataFrame
    user_conversion: pd.DataFrame


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe fichero: {path}")
    return pd.read_csv(path)


def load_uber_exports(folder: str | Path) -> UberLoadBundle:
    folder = Path(folder)
    sot = next(folder.glob("sales-over-time_*.csv"))
    sli = next(folder.glob("sales-leaderboard-items_*.csv"))
    shr = next(folder.glob("sales-hourly_*.csv"))
    ucv = next(folder.glob("user-conversion_*.csv"))

    sales_over_time = _read_csv(sot)
    leaderboard_items = _read_csv(sli)
    sales_hourly = _read_csv(shr)
    user_conversion = _read_csv(ucv)

    return UberLoadBundle(
        sales_over_time=sales_over_time,
        leaderboard_items=leaderboard_items,
        sales_hourly=sales_hourly,
        user_conversion=user_conversion,
    )


def weekly_sales_summary(sales_over_time: pd.DataFrame) -> pd.DataFrame:
    date_col = next((c for c in sales_over_time.columns if c.lower() in {"date", "fecha"}), None)
    sales_col = next((c for c in sales_over_time.columns if "sales" in c.lower() or "venta" in c.lower()), None)
    orders_col = next((c for c in sales_over_time.columns if "order" in c.lower() or "pedido" in c.lower()), None)
    if not date_col or not sales_col:
        raise ValueError("No se encontraron columnas de fecha/ventas en sales-over-time")

    df = sales_over_time.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)
    if orders_col:
        df[orders_col] = pd.to_numeric(df[orders_col], errors="coerce").fillna(0)
    else:
        df["orders_tmp"] = 0
        orders_col = "orders_tmp"

    iso = df[date_col].dt.isocalendar()
    df["anio_iso"] = iso.year
    df["semana_iso"] = iso.week

    out = (
        df.groupby(["anio_iso", "semana_iso"], as_index=False)
        .agg(ventas_totales_bruto=(sales_col, "sum"), num_pedidos=(orders_col, "sum"))
        .sort_values(["anio_iso", "semana_iso"])
    )
    return out
