-- Data warehouse schema for burger BI

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_fecha (
  fecha_id INTEGER PRIMARY KEY,
  fecha DATE NOT NULL UNIQUE,
  dia_semana SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  anio_iso SMALLINT NOT NULL,
  mes SMALLINT NOT NULL,
  trimestre SMALLINT NOT NULL,
  inicio_semana DATE NOT NULL,
  fin_semana DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS dwh.dim_canal (
  canal_id SERIAL PRIMARY KEY,
  canal_nombre TEXT NOT NULL UNIQUE,
  tipo_canal TEXT NOT NULL CHECK (tipo_canal IN ('LOCAL', 'DELIVERY', 'MARKETPLACE'))
);

CREATE TABLE IF NOT EXISTS dwh.dim_producto (
  producto_id SERIAL PRIMARY KEY,
  sku_origen TEXT,
  nombre_origen TEXT NOT NULL,
  nombre_normalizado TEXT NOT NULL,
  categoria TEXT,
  activo BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_producto_nombre_sku
  ON dwh.dim_producto (nombre_normalizado, COALESCE(sku_origen, ''));

CREATE TABLE IF NOT EXISTS dwh.dim_banco (
  banco_id SERIAL PRIMARY KEY,
  nombre_banco TEXT NOT NULL,
  cuenta_alias TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_banco_nombre_alias
  ON dwh.dim_banco (nombre_banco, COALESCE(cuenta_alias, ''));

CREATE TABLE IF NOT EXISTS dwh.dim_proveedor (
  proveedor_id SERIAL PRIMARY KEY,
  nombre_proveedor TEXT NOT NULL UNIQUE,
  nif TEXT
);

CREATE TABLE IF NOT EXISTS dwh.fact_ventas_articulo_semana (
  anio_iso SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  canal_id INTEGER NOT NULL REFERENCES dwh.dim_canal(canal_id),
  producto_id INTEGER NOT NULL REFERENCES dwh.dim_producto(producto_id),
  unidades NUMERIC(12,2) NOT NULL DEFAULT 0,
  importe_neto NUMERIC(14,2) NOT NULL DEFAULT 0,
  importe_bruto NUMERIC(14,2) NOT NULL DEFAULT 0,
  descuentos NUMERIC(14,2) NOT NULL DEFAULT 0,
  impuestos NUMERIC(14,2) NOT NULL DEFAULT 0,
  num_pedidos_con_articulo INTEGER,
  PRIMARY KEY (anio_iso, semana_iso, canal_id, producto_id)
);

CREATE TABLE IF NOT EXISTS dwh.fact_ventas_resumen_semana (
  anio_iso SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  canal_id INTEGER NOT NULL REFERENCES dwh.dim_canal(canal_id),
  ventas_totales_neto NUMERIC(14,2) NOT NULL DEFAULT 0,
  ventas_totales_bruto NUMERIC(14,2) NOT NULL DEFAULT 0,
  num_pedidos INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (anio_iso, semana_iso, canal_id)
);

CREATE TABLE IF NOT EXISTS dwh.fact_proformas_semana (
  anio_iso SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  importe_proformas_emitidas NUMERIC(14,2) NOT NULL DEFAULT 0,
  importe_proformas_cobradas NUMERIC(14,2) NOT NULL DEFAULT 0,
  num_proformas INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (anio_iso, semana_iso)
);

CREATE TABLE IF NOT EXISTS dwh.fact_compras_semana (
  anio_iso SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  proveedor_id INTEGER NOT NULL REFERENCES dwh.dim_proveedor(proveedor_id),
  importe_compras_neto NUMERIC(14,2) NOT NULL DEFAULT 0,
  importe_compras_bruto NUMERIC(14,2) NOT NULL DEFAULT 0,
  num_documentos_compra INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (anio_iso, semana_iso, proveedor_id)
);

CREATE TABLE IF NOT EXISTS dwh.fact_bancos_saldo_semana (
  anio_iso SMALLINT NOT NULL,
  semana_iso SMALLINT NOT NULL,
  banco_id INTEGER NOT NULL REFERENCES dwh.dim_banco(banco_id),
  saldo_inicio_semana NUMERIC(14,2) NOT NULL DEFAULT 0,
  saldo_fin_semana NUMERIC(14,2) NOT NULL DEFAULT 0,
  variacion_semana NUMERIC(14,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (anio_iso, semana_iso, banco_id)
);
