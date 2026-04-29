# Despliegue en Docker Desktop (macOS)


## 0) Configurar variables de entorno (.env)

```bash
cp .env.example .env
```

Edita `.env` y define al menos:
- `HOLDED_API_KEY` (API de Holded)
- `ETL_ADMIN_KEY` (clave para lanzar ETL desde frontend)
- opcionalmente credenciales Postgres

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
