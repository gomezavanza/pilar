# Despliegue en Docker Desktop (macOS)

## 1) Requisitos
- Docker Desktop instalado y arrancado.
- Estar en la raíz del repo.

## 2) Levantar servicios

```bash
docker compose up -d --build
```

Servicios:
- `db` (PostgreSQL + esquema DWH inicial)
- `backend` (job ETL de canales)
- `frontend` (Streamlit dashboard)

## 3) URL del dashboard
- Abrir: http://localhost:8501

## 4) Cargar CSV semanales
Copiar ficheros a:
- `data/inbound/uber/`
- `data/inbound/hiopos/`

Lanzar job manualmente:

```bash
docker compose run --rm backend
```

## 5) Ver logs

```bash
docker compose logs -f frontend
docker compose logs -f backend
docker compose logs -f db
```

## 6) Parar todo

```bash
docker compose down
```

Para borrar también volumen DB:

```bash
docker compose down -v
```
