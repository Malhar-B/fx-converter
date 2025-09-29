from __future__ import annotations
import time
from typing import Any, Dict, Optional
import requests

class ApiError(RuntimeError):
    """Raised for non-OK API responses or exhausted retries."""

class API:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "UTS-FX-Converter/1.0"})

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, retries: int = 2) -> Dict[str, Any]:
        """GET JSON with small retry/backoff."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_exc: Optional[Exception] = None
        for attempt in range(retries + 1):
            try:
                resp = self.session.get(url, params=params or {}, timeout=self.timeout)
                if resp.status_code != 200:
                    raise ApiError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                return resp.json()
            except Exception as exc:
                last_exc = exc
                if attempt < retries:
                    time.sleep(0.6 * (attempt + 1))
        raise ApiError(f"GET {url} failed: {last_exc}")
