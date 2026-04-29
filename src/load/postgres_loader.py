"""Carga básica en PostgreSQL para los hechos semanales."""

from __future__ import annotations

import os
from typing import Iterable, Mapping

import psycopg

REQUIRED_VENTAS_KEYS = {
    "anio_iso",
    "semana_iso",
    "canal_id",
    "ventas_totales_neto",
    "ventas_totales_bruto",
    "num_pedidos",
}


def get_conn() -> psycopg.Connection:
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("Define DATABASE_URL para conectar con PostgreSQL")
    return psycopg.connect(dsn)


def _validate_row(row: Mapping[str, object]) -> None:
    missing = REQUIRED_VENTAS_KEYS - set(row.keys())
    if missing:
        raise ValueError(f"Fila inválida. Faltan columnas requeridas: {sorted(missing)}")


def upsert_ventas_resumen(rows: Iterable[Mapping[str, object]]) -> int:
    rows = list(rows)
    if not rows:
        return 0

    for row in rows:
        _validate_row(row)

    query = """
    INSERT INTO dwh.fact_ventas_resumen_semana (
      anio_iso, semana_iso, canal_id, ventas_totales_neto, ventas_totales_bruto, num_pedidos
    ) VALUES (
      %(anio_iso)s, %(semana_iso)s, %(canal_id)s, %(ventas_totales_neto)s, %(ventas_totales_bruto)s, %(num_pedidos)s
    )
    ON CONFLICT (anio_iso, semana_iso, canal_id)
    DO UPDATE SET
      ventas_totales_neto = EXCLUDED.ventas_totales_neto,
      ventas_totales_bruto = EXCLUDED.ventas_totales_bruto,
      num_pedidos = EXCLUDED.num_pedidos;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, rows)
        conn.commit()
    return len(rows)
