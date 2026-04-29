from __future__ import annotations

from pathlib import Path
from shutil import move
from typing import Iterable

from src.transform.hiopos_parser import parse_hiopos_takeaway_file
from src.transform.uber_parser import parse_uber_weekly_file

INBOUND_UBER = Path("data/inbound/uber")
INBOUND_HIOPOS = Path("data/inbound/hiopos")
ARCHIVE = Path("data/archive")


def _iter_supported_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.glob("*")):
        if path.suffix.lower() in {".csv", ".xlsx", ".xls"} and path.is_file():
            yield path


def _archive_file(path: Path) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    destination = ARCHIVE / path.name
    move(str(path), str(destination))


def run_weekly_channel_job() -> dict[str, int]:
    processed = {"uber": 0, "hiopos": 0}

    INBOUND_UBER.mkdir(parents=True, exist_ok=True)
    INBOUND_HIOPOS.mkdir(parents=True, exist_ok=True)

    for uber_file in _iter_supported_files(INBOUND_UBER):
        parse_uber_weekly_file(uber_file)
        _archive_file(uber_file)
        processed["uber"] += 1

    for hiopos_file in _iter_supported_files(INBOUND_HIOPOS):
        parse_hiopos_takeaway_file(hiopos_file)
        _archive_file(hiopos_file)
        processed["hiopos"] += 1

    return processed


if __name__ == "__main__":
    result = run_weekly_channel_job()
    print(f"Procesados: UBER={result['uber']} HIOPOS={result['hiopos']}")
