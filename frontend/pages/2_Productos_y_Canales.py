from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="BI Productos y Canales", layout="wide")
st.title("🍔 Productos y Canales")

DB_URL = os.getenv("DATABASE_URL")


@st.cache_data(ttl=300)
def load_product_channel_weekly() -> pd.DataFrame:
    if not DB_URL:
        return pd.DataFrame([
            {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "HIOPOS_LOCAL", "producto": "Cheeseburger", "unidades": 240, "importe_bruto": 2880},
            {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "UBER_EATS", "producto": "Cheeseburger", "unidades": 110, "importe_bruto": 1540},
            {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "HIOPOS_LOCAL", "producto": "Patatas", "unidades": 210, "importe_bruto": 945},
            {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "UBER_EATS", "producto": "Patatas", "unidades": 90, "importe_bruto": 495},
        ])

    engine = create_engine(DB_URL)
    query = text(
        """
        SELECT f.anio_iso, f.semana_iso, c.canal_nombre, p.nombre_normalizado AS producto, f.unidades, f.importe_bruto
        FROM dwh.fact_ventas_articulo_semana f
        JOIN dwh.dim_canal c ON c.canal_id = f.canal_id
        JOIN dwh.dim_producto p ON p.producto_id = f.producto_id
        ORDER BY f.anio_iso, f.semana_iso, c.canal_nombre, p.nombre_normalizado;
        """
    )
    with engine.begin() as conn:
        return pd.read_sql(query, conn)


df = load_product_channel_weekly()
if df.empty:
    st.warning("No hay datos de artículos para mostrar.")
    st.stop()

df["periodo"] = df["anio_iso"].astype(str) + "-W" + df["semana_iso"].astype(str).str.zfill(2)

# dynamic filters + drilldown
week = st.sidebar.selectbox("Semana", sorted(df["periodo"].unique()), index=len(df["periodo"].unique()) - 1)
channels = st.sidebar.multiselect("Canales", sorted(df["canal_nombre"].unique()), default=sorted(df["canal_nombre"].unique()))
products = st.sidebar.multiselect("Productos", sorted(df["producto"].unique()), default=sorted(df["producto"].unique()))
metric = st.sidebar.selectbox("Métrica", ["importe_bruto", "unidades"], index=0)

filtered = df[(df["periodo"] == week) & (df["canal_nombre"].isin(channels)) & (df["producto"].isin(products))]

st.subheader("Top productos")
agg_prod = filtered.groupby("producto", as_index=False)[metric].sum().sort_values(metric, ascending=False)
st.plotly_chart(px.bar(agg_prod.head(10), x="producto", y=metric), use_container_width=True)

st.subheader("Drilldown canal -> producto")
selected_channel = st.selectbox("Canal detalle", sorted(filtered["canal_nombre"].unique()))
channel_df = filtered[filtered["canal_nombre"] == selected_channel]
st.dataframe(channel_df.sort_values(metric, ascending=False), use_container_width=True)
