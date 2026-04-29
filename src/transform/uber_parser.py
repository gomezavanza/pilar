from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class UberWeeklyResult:
    ventas_articulos: pd.DataFrame
    resumen: pd.DataFrame


COLUMN_ALIASES = {
    "articulo": ["Artículo", "Articulo", "Item name", "Menu Item"],
    "unidades": ["Cantidad", "Units sold", "Unidades"],
    "ventas_totales": ["Ventas", "Gross sales", "Total sales", "Ventas totales"],
    "num_pedidos": ["Pedidos", "Orders", "Nº de pedidos", "Numero de pedidos"],
}


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    raise ValueError(f"No se encontró ninguna columna válida entre: {candidates}")


def parse_uber_weekly_file(path: str | Path) -> UberWeeklyResult:
    """Parsea export semanal de Uber (CSV/XLSX) y normaliza outputs."""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError("Formato no soportado. Usa CSV o Excel.")

    col_articulo = _pick_column(df, COLUMN_ALIASES["articulo"])
    col_unidades = _pick_column(df, COLUMN_ALIASES["unidades"])
    col_ventas = _pick_column(df, COLUMN_ALIASES["ventas_totales"])

    items = df[[col_articulo, col_unidades, col_ventas]].rename(
        columns={
            col_articulo: "articulo",
            col_unidades: "unidades",
            col_ventas: "ventas_totales",
        }
    )
    items["unidades"] = pd.to_numeric(items["unidades"], errors="coerce").fillna(0)
    items["ventas_totales"] = pd.to_numeric(items["ventas_totales"], errors="coerce").fillna(0)

    total_ventas = float(items["ventas_totales"].sum())

    col_pedidos = None
    for candidate in COLUMN_ALIASES["num_pedidos"]:
        if candidate in df.columns:
            col_pedidos = candidate
            break

    num_pedidos = int(pd.to_numeric(df[col_pedidos], errors="coerce").fillna(0).sum()) if col_pedidos else 0
    ticket_medio = (total_ventas / num_pedidos) if num_pedidos else 0.0

    resumen = pd.DataFrame(
        [
            {
                "canal": "UBER_EATS",
                "ventas_totales": total_ventas,
                "num_pedidos": num_pedidos,
                "ticket_medio": ticket_medio,
            }
        ]
    )
    return UberWeeklyResult(ventas_articulos=items, resumen=resumen)
