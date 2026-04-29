from datetime import date, datetime
from unittest.mock import Mock

import pytest

from src.extract.holded_api import HoldedClient, _to_epoch_seconds


def test_to_epoch_seconds_accepts_date_and_datetime() -> None:
    assert _to_epoch_seconds(date(1970, 1, 1)) == 0
    assert _to_epoch_seconds(datetime(1970, 1, 1)) == 0


def test_get_returns_list_and_wraps_dict() -> None:
    session = Mock()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"ok": True}
    session.get.return_value = response

    client = HoldedClient(api_key="x", session=session)
    out = client.bancos()

    assert out == [{"ok": True}]


def test_get_raises_for_unexpected_payload() -> None:
    session = Mock()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = "bad"
    session.get.return_value = response

    client = HoldedClient(api_key="x", session=session)
    with pytest.raises(ValueError):
        client.bancos()
