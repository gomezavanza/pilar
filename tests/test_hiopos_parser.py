from pathlib import Path

from src.transform.hiopos_parser import parse_hiopos_takeaway_file


def test_parse_hiopos_takeaway_csv(tmp_path: Path) -> None:
    path = tmp_path / "hiopos_takeaway.csv"
    path.write_text(
        "Artículo,Cantidad,Importe,Pedidos\n"
        "Cheeseburger,8,96,2\n"
        "Patatas,4,16,2\n",
        encoding="utf-8",
    )

    result = parse_hiopos_takeaway_file(path)

    assert list(result.ventas_articulos.columns) == ["articulo", "unidades", "ventas_totales"]
    assert float(result.resumen.iloc[0]["ventas_totales"]) == 112.0
    assert int(result.resumen.iloc[0]["num_pedidos"]) == 4
