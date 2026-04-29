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
        return pd.DataFrame(
            [
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "HIOPOS_LOCAL", "producto": "Cheeseburger", "unidades": 240, "importe_bruto": 2880},
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "UBER_EATS", "producto": "Cheeseburger", "unidades": 110, "importe_bruto": 1540},
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "HIOPOS_LOCAL", "producto": "Patatas", "unidades": 210, "importe_bruto": 945},
                {"anio_iso": 2026, "semana_iso": 16, "canal_nombre": "UBER_EATS", "producto": "Patatas", "unidades": 90, "importe_bruto": 495},
            ]
        )

    engine = create_engine(DB_URL)
    query = text(
        """
        SELECT
          f.anio_iso,
          f.semana_iso,
          c.canal_nombre,
          p.nombre_normalizado AS producto,
          f.unidades,
          f.importe_bruto
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

colf1, colf2 = st.columns(2)
with colf1:
    semana_sel = st.selectbox("Semana", sorted(df["periodo"].unique()), index=len(df["periodo"].unique()) - 1)
with colf2:
    canales_sel = st.multiselect("Canales", sorted(df["canal_nombre"].unique()), default=sorted(df["canal_nombre"].unique()))

filtered = df[(df["periodo"] == semana_sel) & (df["canal_nombre"].isin(canales_sel))]

st.subheader("Top productos por ventas")
top_products = (
    filtered.groupby("producto", as_index=False)["importe_bruto"].sum().sort_values("importe_bruto", ascending=False).head(10)
)
fig_top = px.bar(top_products, x="producto", y="importe_bruto")
st.plotly_chart(fig_top, use_container_width=True)

st.subheader("Comparativa Uber vs Hiopos (ventas)")
channel_sales = filtered.groupby("canal_nombre", as_index=False)["importe_bruto"].sum()
fig_channels = px.pie(channel_sales, values="importe_bruto", names="canal_nombre")
st.plotly_chart(fig_channels, use_container_width=True)

st.subheader("Detalle por artículo")
st.dataframe(filtered.sort_values(["canal_nombre", "importe_bruto"], ascending=[True, False]), use_container_width=True)
