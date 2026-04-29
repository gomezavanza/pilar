# Frontend BI (Streamlit)

## Ejecutar en local

```bash
python -m pip install -r requirements.txt
python -m pip install -r frontend/requirements-frontend.txt
streamlit run frontend/app.py
```

## Configuración de datos

- Si existe `DATABASE_URL`, la app consulta tablas DWH.
- Si no existe `DATABASE_URL`, la app muestra datos demo para validar la UI.

## Páginas incluidas

1. **Resumen Ejecutivo** (`frontend/app.py`)
   - KPIs: ventas totales, nº pedidos, ticket medio.
   - Gráfico de barras: ventas por semana y canal.
   - Gráfico de líneas: pedidos por semana y canal.
   - Tabla de detalle semanal.

2. **Productos y Canales** (`frontend/pages/2_Productos_y_Canales.py`)
   - Top productos por ventas en la semana seleccionada.
   - Comparativa de ventas por canal (Uber vs Hiopos u otros).
   - Tabla de detalle por artículo/canal/semana.
