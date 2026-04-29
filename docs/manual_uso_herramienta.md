# Manual de uso de la herramienta BI

## 1. Objetivo
La herramienta permite visualizar y analizar ventas, pedidos y rendimiento por canal/producto, además de lanzar procesos ETL semanales.

## 2. Navegación
La app tiene dos páginas:
1. **BI Hamburguesería** (resumen ejecutivo)
2. **Productos y Canales** (detalle por artículo)

## 3. Página "BI Hamburguesería"
### Filtros
En la barra lateral:
- Rango de semanas
- Canales
- Métrica principal (ventas/pedidos)

### KPIs
- Ventas totales
- Nº pedidos
- Ticket medio
- Variación WoW (semana contra semana)

### Drilldown
- Seleccionar semana
- Seleccionar canal
- Revisar tabla detalle

### Visuales
- Evolución semanal (barras)
- Mix por canal (pie)

## 4. Página "Productos y Canales"
### Filtros
- Semana
- Canales
- Productos
- Métrica (importe/unidades)

### Drilldown
- Top productos
- Detalle por canal -> producto

## 5. Ejecución ETL desde frontend
En "Operación ETL (opcional)":
1. Introducir `Clave admin ETL`.
2. Pulsar `Ejecutar job semanal de canales`.
3. Revisar mensaje de éxito/error.

## 6. Flujo operativo recomendado semanal
1. Exportar ficheros Uber y Hiopos.
2. Copiarlos a carpetas `data/inbound/...`.
3. Ejecutar ETL (desde UI o backend).
4. Validar KPIs en dashboard.
5. Revisar tendencias y outliers.

## 7. Buenas prácticas
- Cerrar semana antes de compartir KPIs.
- Validar ticket medio y pedidos cada semana.
- Controlar canales sin datos (posible fallo de carga).
- Mantener histórico de fuentes en `data/archive`.
