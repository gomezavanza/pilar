# Checklist operativo semanal (BI Hamburguesería)

## 1) Recolección de datos
- [ ] Descargar export semanal de Uber (artículos, ventas totales, pedidos, ticket medio).
- [ ] Descargar export semanal de Hiopos con las mismas métricas.
- [ ] Verificar que los archivos incluyan fecha/semana identificable.

## 2) Carga en sistema
- [ ] Copiar archivos en `data/inbound/uber/` y `data/inbound/hiopos/`.
- [ ] Ejecutar job de carga semanal de canales.
- [ ] Ejecutar extracción de Holded (ventas, proformas, compras, bancos).

## 3) Validaciones de calidad
- [ ] Revisar log ETL: filas cargadas y errores.
- [ ] Confirmar que no hay duplicados por semana/canal/artículo.
- [ ] Validar ticket medio recalculado vs informado (tolerancia ±1%).
- [ ] Revisar outliers de ventas WoW (>40%).

## 4) Publicación
- [ ] Refrescar dashboard.
- [ ] Verificar KPIs principales de la semana.
- [ ] Compartir resumen ejecutivo con operaciones/gerencia.

## 5) Cierre
- [ ] Archivar ficheros fuente de la semana.
- [ ] Registrar incidencias y acciones correctivas.

## 6) Automatización opcional (ya disponible)
- [ ] Ejecutar `python -m src.jobs.job_weekly_channels` para procesar automáticamente CSV/XLSX/XLS de `data/inbound/uber/` y `data/inbound/hiopos/`.
- [ ] Verificar que los ficheros procesados se mueven a `data/archive/`.
