from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class HioposWeeklyResult:
    ventas_articulos: pd.DataFrame
    resumen: pd.DataFrame


COLUMN_ALIASES = {
    "articulo": ["Artículo", "Articulo", "Producto", "Item"],
    "unidades": ["Cantidad", "Unidades", "Qty"],
    "ventas_totales": ["Importe", "Ventas", "Total", "Ventas totales"],
}


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for c in candidates:
        if c in df.columns:
            return c
    raise ValueError(f"No se encontró columna en: {candidates}")


def parse_hiopos_takeaway_file(path: str | Path) -> HioposWeeklyResult:
    """Parsea reporte de HIOPOS (ventas por artículos) para canal Take Away."""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError("Formato no soportado. Usa CSV o Excel.")

    col_articulo = _pick_column(df, COLUMN_ALIASES["articulo"])
    col_unidades = _pick_column(df, COLUMN_ALIASES["unidades"])
    col_importe = _pick_column(df, COLUMN_ALIASES["ventas_totales"])

    items = df[[col_articulo, col_unidades, col_importe]].rename(
        columns={col_articulo: "articulo", col_unidades: "unidades", col_importe: "ventas_totales"}
    )
    items["unidades"] = pd.to_numeric(items["unidades"], errors="coerce").fillna(0)
    items["ventas_totales"] = pd.to_numeric(items["ventas_totales"], errors="coerce").fillna(0)

    ventas_totales = float(items["ventas_totales"].sum())
    num_pedidos = 0
    ticket_medio = 0.0
    if "Pedidos" in df.columns:
        num_pedidos = int(pd.to_numeric(df["Pedidos"], errors="coerce").fillna(0).sum())
        ticket_medio = ventas_totales / num_pedidos if num_pedidos else 0.0

    resumen = pd.DataFrame(
        [{"canal": "HIOPOS_TAKE_AWAY", "ventas_totales": ventas_totales, "num_pedidos": num_pedidos, "ticket_medio": ticket_medio}]
    )
    return HioposWeeklyResult(ventas_articulos=items, resumen=resumen)
