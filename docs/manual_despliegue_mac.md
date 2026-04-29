# Manual de despliegue en macOS (Docker Desktop)

## 1. Prerrequisitos
- macOS con Docker Desktop instalado y en ejecución.
- Git instalado.
- Acceso al repositorio del proyecto.

## 2. Preparar proyecto
```bash
git clone <URL_REPO>
cd pilar
cp .env.example .env
```

Editar `.env`:
- `HOLDED_API_KEY`: clave API de Holded.
- `ETL_ADMIN_KEY`: clave para proteger el botón ETL del frontend.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: credenciales de base de datos.

## 3. Levantar stack completo
```bash
docker compose up -d --build
```

Servicios desplegados:
- `db`: PostgreSQL con inicialización automática de `sql/dwh_schema.sql`.
- `backend`: runner del job ETL de canales.
- `frontend`: Streamlit en puerto `8501`.

## 4. Verificar estado
```bash
docker compose ps
docker compose logs -f frontend
```

Abrir navegador:
- http://localhost:8501

## 5. Carga de ficheros operativos
Copiar exportes:
- Uber: `data/inbound/uber/`
- Hiopos: `data/inbound/hiopos/`

Ejecutar job ETL manual:
```bash
docker compose run --rm backend
```

## 6. Mantenimiento
### Reiniciar servicios
```bash
docker compose restart
```

### Parar servicios
```bash
docker compose down
```

### Parar y eliminar datos de DB
```bash
docker compose down -v
```

## 7. Troubleshooting rápido
- **No abre frontend**: revisar `docker compose logs -f frontend`.
- **Error de conexión DB**: validar variables `POSTGRES_*` en `.env`.
- **ETL no corre desde UI**: comprobar `ETL_ADMIN_KEY` y que la clave introducida coincida.
- **No carga Holded**: verificar `HOLDED_API_KEY` válida.
