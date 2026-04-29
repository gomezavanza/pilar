import pytest

from src.load.postgres_loader import _validate_row, upsert_ventas_resumen


def test_validate_row_missing_keys() -> None:
    with pytest.raises(ValueError):
        _validate_row({"anio_iso": 2026})


def test_upsert_returns_zero_on_empty_rows() -> None:
    assert upsert_ventas_resumen([]) == 0
