from pathlib import Path

from src.jobs.job_weekly_channels import ARCHIVE, INBOUND_HIOPOS, INBOUND_UBER, run_weekly_channel_job


def test_run_weekly_channel_job_moves_files(tmp_path: Path, monkeypatch) -> None:
    inbound_uber = tmp_path / "data/inbound/uber"
    inbound_hiopos = tmp_path / "data/inbound/hiopos"
    archive = tmp_path / "data/archive"
    inbound_uber.mkdir(parents=True)
    inbound_hiopos.mkdir(parents=True)

    (inbound_uber / "uber.csv").write_text("Artículo,Cantidad,Ventas,Pedidos\nA,1,10,1\n", encoding="utf-8")
    (inbound_hiopos / "hiopos.csv").write_text("Artículo,Cantidad,Importe,Pedidos\nB,2,20,1\n", encoding="utf-8")

    monkeypatch.setattr("src.jobs.job_weekly_channels.INBOUND_UBER", inbound_uber)
    monkeypatch.setattr("src.jobs.job_weekly_channels.INBOUND_HIOPOS", inbound_hiopos)
    monkeypatch.setattr("src.jobs.job_weekly_channels.ARCHIVE", archive)

    result = run_weekly_channel_job()

    assert result == {"uber": 1, "hiopos": 1}
    assert (archive / "uber.csv").exists()
    assert (archive / "hiopos.csv").exists()
