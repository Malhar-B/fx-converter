from __future__ import annotations
from typing import Dict, Tuple, List
from api import API

_api = API("https://api.frankfurter.app")

def list_currencies() -> Dict[str, str]:
    """Map currency code -> full name. GET /currencies"""
    data = _api.get("/currencies")
    if not isinstance(data, dict) or not data:
        raise RuntimeError("Unexpected currencies payload")
    return data

def get_latest_rate(from_ccy: str, to_ccy: str) -> Tuple[str, float]:
    """(date_iso, rate) for the latest day. GET /latest?from=...&to=..."""
    if from_ccy == to_ccy:
        return (today_iso(), 1.0)
    payload = _api.get("/latest", params={"from": from_ccy, "to": to_ccy})
    date = payload.get("date")
    rates = payload.get("rates", {})
    if date is None or to_ccy not in rates:
        raise RuntimeError(f"Missing rate for {from_ccy}->{to_ccy}")
    return date, float(rates[to_ccy])

def get_rate_on(date_iso: str, from_ccy: str, to_ccy: str) -> Tuple[str, float]:
    """(date_iso_from_api, rate) for a given date. GET /{date}?from=...&to=..."""
    if from_ccy == to_ccy:
        return (date_iso, 1.0)
    payload = _api.get(f"/{date_iso}", params={"from": from_ccy, "to": to_ccy})
    date = payload.get("date", date_iso)
    rates = payload.get("rates", {})
    if to_ccy not in rates:
        raise RuntimeError(f"No historical rate for {date} {from_ccy}->{to_ccy}")
    return date, float(rates[to_ccy])

def get_timeseries(from_ccy: str, to_ccy: str, start_iso: str, end_iso: str) -> List[Dict[str, float]]:
    """Optional helper for chart: /start..end?from=...&to=..."""
    if from_ccy == to_ccy:
        return []
    payload = _api.get(f"/{start_iso}..{end_iso}", params={"from": from_ccy, "to": to_ccy})
    rates = payload.get("rates", {})
    return [{"date": d, "rate": float(v[to_ccy])} for d, v in sorted(rates.items()) if to_ccy in v]

def today_iso() -> str:
    from datetime import date
    return date.today().isoformat()
