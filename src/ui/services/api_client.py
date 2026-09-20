"""Base API Client with fast offline detection, timeouts, and instantaneous mock fallbacks."""

import os
from typing import Any, Dict, Optional
import requests


class APIClient:
    """HTTP client for backend communication with zero-latency offline degradation."""

    _backend_checked: bool = False
    _backend_available: bool = False

    def __init__(self, base_url: Optional[str] = None, timeout: float = 0.5):
        self.base_url = (base_url or os.environ.get("BACKEND_API_URL", "http://localhost:8000")).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def check_connection(self, force: bool = False) -> bool:
        """Quickly check backend connectivity with minimal timeout once per lifecycle."""
        if APIClient._backend_checked and not force:
            return APIClient._backend_available

        try:
            url = f"{self.base_url}/health"
            res = self.session.get(url, timeout=0.15)
            APIClient._backend_available = (res.status_code == 200)
        except Exception:
            APIClient._backend_available = False

        APIClient._backend_checked = True
        return APIClient._backend_available

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self.check_connection():
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            APIClient._backend_available = False
            return None

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self.check_connection():
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            APIClient._backend_available = False
            return None

    def is_alive(self) -> bool:
        """Check if live backend server is reachable."""
        return self.check_connection()

