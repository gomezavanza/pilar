# Frontend BI (Streamlit)

## Ejecutar en local

```bash
python -m pip install -r requirements.txt
python -m pip install -r frontend/requirements-frontend.txt
streamlit run frontend/app.py
```

## Configuración de datos

- Si existe `DATABASE_URL`, la app consulta `dwh.fact_ventas_resumen_semana` + `dwh.dim_canal`.
- Si no existe `DATABASE_URL`, la app muestra datos demo para poder validar la UI.

## Vistas incluidas

- KPIs: ventas totales, nº pedidos, ticket medio.
- Gráfico de barras: ventas por semana y canal.
- Gráfico de líneas: pedidos por semana y canal.
- Tabla de detalle semanal.
