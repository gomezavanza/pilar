from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

from src.analytics.kpis import build_weekly_totals, calc_ticket_medio, calc_wow

st.set_page_config(page_title="BI Hamburguesería", layout="wide")
st.title("📊 BI Hamburguesería")

DB_URL = os.getenv("DATABASE_URL")


@st.cache_data(ttl=300)
def load_weekly_sales() -> pd.DataFrame:
    if not DB_URL:
        return pd.DataFrame(
            [
                {"anio_iso": 2026, "semana_iso": 15, "canal_nombre": "HIOPOS_LOCAL", "ventas_totales_bruto": 12350.0, "num_pedidos": 490},
                {"anio_iso": 2026, "semana_iso": 15, "canal_nombre": "UBER_EATS", "ventas_totales_bruto": 4200.0, "num_pedidos": 180},
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "HIOPOS_LOCAL", "ventas_totales_bruto": 13200.0, "num_pedidos": 510},
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "UBER_EATS", "ventas_totales_bruto": 4600.0, "num_pedidos": 200},
            ]
        )

    engine = create_engine(DB_URL)
    query = text(
        """
        SELECT
          f.anio_iso,
          f.semana_iso,
          c.canal_nombre,
          f.ventas_totales_bruto,
          f.num_pedidos,
          CASE WHEN f.num_pedidos = 0 THEN 0
               ELSE f.ventas_totales_bruto / f.num_pedidos END AS ticket_medio
        FROM dwh.fact_ventas_resumen_semana f
        JOIN dwh.dim_canal c ON c.canal_id = f.canal_id
        ORDER BY f.anio_iso, f.semana_iso, c.canal_nombre;
        """
    )
    with engine.begin() as conn:
        return pd.read_sql(query, conn)


df = load_weekly_sales()

if df.empty:
    st.warning("No hay datos para mostrar todavía.")
    st.stop()

# Filters
canales = st.multiselect("Canales", sorted(df["canal_nombre"].unique()), default=sorted(df["canal_nombre"].unique()))
df_filtered = df[df["canal_nombre"].isin(canales)].copy()
df_filtered["periodo"] = df_filtered["anio_iso"].astype(str) + "-W" + df_filtered["semana_iso"].astype(str).str.zfill(2)

# KPIs
col1, col2, col3, col4 = st.columns(4)
ventas_total = float(df_filtered["ventas_totales_bruto"].sum())
pedidos_total = int(df_filtered["num_pedidos"].sum())
ticket_medio = calc_ticket_medio(ventas_total, pedidos_total)

weekly_totals = build_weekly_totals(df_filtered)
wow = 0.0
if len(weekly_totals) > 1:
    wow = calc_wow(float(weekly_totals.iloc[-1]["ventas_totales_bruto"]), float(weekly_totals.iloc[-2]["ventas_totales_bruto"]))

col1.metric("Ventas totales", f"€ {ventas_total:,.2f}")
col2.metric("Nº pedidos", f"{pedidos_total:,}")
col3.metric("Ticket medio", f"€ {ticket_medio:,.2f}")
col4.metric("WoW ventas", f"{wow:,.1f}%")

# Charts
left, right = st.columns(2)
with left:
    st.subheader("Ventas por semana")
    chart_sales = px.bar(
        df_filtered,
        x="periodo",
        y="ventas_totales_bruto",
        color="canal_nombre",
        barmode="group",
    )
    st.plotly_chart(chart_sales, use_container_width=True)

with right:
    st.subheader("Pedidos por semana")
    chart_orders = px.line(
        df_filtered,
        x="periodo",
        y="num_pedidos",
        color="canal_nombre",
        markers=True,
    )
    st.plotly_chart(chart_orders, use_container_width=True)

# Table
st.subheader("Detalle semanal")
view_df = df_filtered.copy()
view_df["ticket_medio"] = view_df.apply(
    lambda row: (row["ventas_totales_bruto"] / row["num_pedidos"]) if row["num_pedidos"] else 0,
    axis=1,
)
st.dataframe(view_df, use_container_width=True)
