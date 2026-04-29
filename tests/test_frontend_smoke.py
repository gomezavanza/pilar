from pathlib import Path


def test_frontend_contains_etl_button_and_admin_key() -> None:
    content = Path("frontend/app.py").read_text(encoding="utf-8")
    assert "Ejecutar job semanal de canales" in content
    assert "ETL_ADMIN_KEY" in content
    assert "Clave admin ETL" in content


def test_frontend_contains_filters_and_drilldown() -> None:
    content = Path("frontend/app.py").read_text(encoding="utf-8")
    assert "Filtros globales" in content
    assert "Drilldown ventas" in content
