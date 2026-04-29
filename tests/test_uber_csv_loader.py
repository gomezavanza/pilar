from pathlib import Path

from src.load.uber_csv_loader import load_uber_exports, weekly_sales_summary


def test_load_uber_exports_and_weekly_summary(tmp_path: Path) -> None:
    (tmp_path / "sales-over-time_2025.csv").write_text("Date,Sales,Orders\n2026-01-01,100,5\n2026-01-02,50,3\n", encoding="utf-8")
    (tmp_path / "sales-leaderboard-items_2025.csv").write_text("Item,Sales\nBurger,50\n", encoding="utf-8")
    (tmp_path / "sales-hourly_2025.csv").write_text("Hour,Sales\n10,20\n", encoding="utf-8")
    (tmp_path / "user-conversion_2025.csv").write_text("Step,Count\nView,10\n", encoding="utf-8")

    bundle = load_uber_exports(tmp_path)
    summary = weekly_sales_summary(bundle.sales_over_time)

    assert len(bundle.sales_over_time) == 2
    assert float(summary.iloc[0]["ventas_totales_bruto"]) == 150.0
    assert int(summary.iloc[0]["num_pedidos"]) == 8
