from __future__ import annotations

import os
import subprocess

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

from src.analytics.kpis import build_weekly_totals, calc_ticket_medio, calc_wow

st.set_page_config(page_title="BI Hamburguesería", layout="wide")
st.title("📊 BI Hamburguesería")

DB_URL = os.getenv("DATABASE_URL")
ETL_ADMIN_KEY = os.getenv("ETL_ADMIN_KEY")


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
        SELECT f.anio_iso, f.semana_iso, c.canal_nombre, f.ventas_totales_bruto, f.num_pedidos
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

df["periodo"] = df["anio_iso"].astype(str) + "-W" + df["semana_iso"].astype(str).str.zfill(2)

# Sidebar dynamic filters
st.sidebar.header("Filtros globales")
weeks = sorted(df["periodo"].unique())
week_range = st.sidebar.select_slider("Rango de semanas", options=weeks, value=(weeks[0], weeks[-1]))
canales = st.sidebar.multiselect("Canales", sorted(df["canal_nombre"].unique()), default=sorted(df["canal_nombre"].unique()))
metric = st.sidebar.selectbox("Métrica principal", ["ventas_totales_bruto", "num_pedidos"], index=0)

min_i, max_i = weeks.index(week_range[0]), weeks.index(week_range[1])
valid_weeks = set(weeks[min_i : max_i + 1])
df_filtered = df[(df["periodo"].isin(valid_weeks)) & (df["canal_nombre"].isin(canales))].copy()

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

# Drilldown: semana -> canal
st.subheader("Drilldown ventas")
sel_week = st.selectbox("Selecciona semana", sorted(df_filtered["periodo"].unique(), reverse=True))
week_df = df_filtered[df_filtered["periodo"] == sel_week]
sel_channel = st.selectbox("Selecciona canal", sorted(week_df["canal_nombre"].unique()))
channel_df = week_df[week_df["canal_nombre"] == sel_channel]
st.dataframe(channel_df, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Evolución semanal")
    chart_sales = px.bar(df_filtered, x="periodo", y=metric, color="canal_nombre", barmode="group")
    st.plotly_chart(chart_sales, use_container_width=True)
with right:
    st.subheader("Mix por canal")
    pie = df_filtered.groupby("canal_nombre", as_index=False)["ventas_totales_bruto"].sum()
    st.plotly_chart(px.pie(pie, values="ventas_totales_bruto", names="canal_nombre"), use_container_width=True)

with st.expander("Operación ETL (opcional)"):
    st.caption("Procesa ficheros en data/inbound/* y los mueve a data/archive.")
    user_key = st.text_input("Clave admin ETL", type="password")
    if st.button("Ejecutar job semanal de canales"):
        if ETL_ADMIN_KEY and user_key != ETL_ADMIN_KEY:
            st.error("Clave ETL incorrecta")
        else:
            run = subprocess.run(["python", "-m", "src.jobs.job_weekly_channels"], capture_output=True, text=True)
            if run.returncode == 0:
                st.success(run.stdout.strip() or "Job ejecutado correctamente")
            else:
                st.error("Error ejecutando el job")
                st.code(run.stderr or run.stdout)
