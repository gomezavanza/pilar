from pathlib import Path

from src.transform.uber_parser import parse_uber_weekly_file


def test_parse_uber_weekly_file_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "uber.csv"
    csv_path.write_text(
        "Artículo,Cantidad,Ventas,Pedidos\n"
        "Cheeseburger,10,120,3\n"
        "Patatas,5,20,3\n",
        encoding="utf-8",
    )

    result = parse_uber_weekly_file(csv_path)

    assert set(result.ventas_articulos.columns) == {"articulo", "unidades", "ventas_totales"}
    assert float(result.resumen.iloc[0]["ventas_totales"]) == 140.0
    assert int(result.resumen.iloc[0]["num_pedidos"]) == 6
