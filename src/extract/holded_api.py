"""Extractores de Holded para ventas, proformas, compras y bancos."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

import requests

BASE_URL = "https://api.holded.com/api"


def _to_epoch_seconds(value: date | datetime) -> int:
    """Convierte fechas/datetimes a epoch seconds (UTC)."""
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime(value.year, value.month, value.day, tzinfo=timezone.utc)
    elif value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return int(value.timestamp())


@dataclass
class HoldedClient:
    api_key: str
    timeout_seconds: int = 30
    session: Optional[requests.Session] = None

    @classmethod
    def from_env(cls) -> "HoldedClient":
        api_key = os.getenv("HOLDED_API_KEY")
        if not api_key:
            raise RuntimeError("Falta HOLDED_API_KEY en variables de entorno.")
        return cls(api_key=api_key)

    def _headers(self) -> Dict[str, str]:
        return {
            "accept": "application/json",
            "key": self.api_key,
        }

    def _http_get(self, url: str, params: Dict[str, Any]) -> requests.Response:
        client = self.session or requests
        return client.get(url, headers=self._headers(), params=params, timeout=self.timeout_seconds)

    def _get(self, endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        url = f"{BASE_URL}/{endpoint}"
        response = self._http_get(url, params)
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            return [payload]
        raise ValueError(f"Respuesta inesperada en {endpoint}: {type(payload)!r}")

    def ventas(self, start: date | datetime, end: date | datetime) -> List[Dict[str, Any]]:
        return self._get("invoicing/v1/documents/invoice", {"starttmp": _to_epoch_seconds(start), "endtmp": _to_epoch_seconds(end)})

    def proformas(self, start: date | datetime, end: date | datetime) -> List[Dict[str, Any]]:
        return self._get("invoicing/v1/documents/proform", {"starttmp": _to_epoch_seconds(start), "endtmp": _to_epoch_seconds(end)})

    def compras(self, start: date | datetime, end: date | datetime) -> List[Dict[str, Any]]:
        return self._get("invoicing/v1/documents/purchase", {"starttmp": _to_epoch_seconds(start), "endtmp": _to_epoch_seconds(end)})

    def bancos(self) -> List[Dict[str, Any]]:
        return self._get("banking/v1/account", {})
