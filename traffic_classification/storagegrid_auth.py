#!/usr/bin/env python3
"""Authenticate to StorageGRID and run a basic health check.

Usage:
    storagegrid_auth.py --auth-config auth.local.yaml

Import StorageGRIDClient/load_yaml/resolve_connection from this module to
build other StorageGRID scripts (see storagegrid_traffic_classification.py).
"""

import argparse
import json
import os
import sys
from typing import Any

import requests
import urllib3
import yaml


HEALTH_PATH = "/api/v3/grid/config/product-version"


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

def load_yaml(path: str | None, default: Any = None) -> Any:
    """Load a YAML file, or return `default` if no path was given."""
    if not path:
        return default
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return default if data is None else data


def resolve_connection(args: argparse.Namespace, auth_config: dict[str, Any]) -> dict[str, Any]:
    """Merge CLI flags, the auth config file, and environment variables into connection settings.

    Precedence: CLI flag > auth config file > environment variable.
    """
    auth_config = auth_config or {}

    host = args.host or auth_config.get("host") or os.getenv("STORAGEGRID_HOST")
    username = args.username or auth_config.get("username") or os.getenv("STORAGEGRID_USERNAME")
    password = args.password or auth_config.get("password") or os.getenv("STORAGEGRID_PASSWORD")
    ca_bundle = args.ca_bundle or auth_config.get("ca_bundle") or os.getenv("STORAGEGRID_CA_BUNDLE")
    insecure = args.insecure or bool(auth_config.get("insecure", False))

    missing = [name for name, value in (("host", host), ("username", username), ("password", password)) if not value]
    if missing:
        raise SystemExit(
            "Missing required connection settings: " + ", ".join(missing) +
            ". Provide them via --auth-config, CLI flags, or STORAGEGRID_* environment variables."
        )

    return {
        "host": host,
        "username": username,
        "password": password,
        "verify": False if insecure else (ca_bundle or True),
    }


# --------------------------------------------------------------------------
# HTTP / authentication helpers
# --------------------------------------------------------------------------

def normalize_host(host: str) -> str:
    """Add the default HTTPS scheme when the host is supplied as an IP or name."""
    host = host.strip().rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = f"https://{host}"
    return host


def extract_token(response: requests.Response) -> str:
    """Extract a StorageGRID bearer token from supported authorization responses."""
    payload = response.json()
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        token_keys = ("token", "apiToken", "access_token", "accessToken")
        values = [payload]
        while values:
            value = values.pop()
            if isinstance(value, dict):
                for key in token_keys:
                    if isinstance(value.get(key), str):
                        return value[key]
                data = value.get("data")
                if isinstance(data, str) and data:
                    return data
                values.extend(item for key, item in value.items() if key != "data")
            elif isinstance(value, list):
                values.extend(value)
    response_keys = ", ".join(payload.keys()) if isinstance(payload, dict) else type(payload).__name__
    raise ValueError(
        "StorageGRID authorization response did not contain a bearer token "
        f"(response keys/type: {response_keys})"
    )


# --------------------------------------------------------------------------
# StorageGRID client (generic - no policy-specific knowledge)
# --------------------------------------------------------------------------

class StorageGRIDClient:
    """Authenticated HTTP client for the StorageGRID Grid Management API.

    Pass account_id to authenticate as a tenant's root user instead of a grid admin.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        verify: bool | str = True,
        account_id: str | None = None,
    ):
        self.base_url = normalize_host(host)
        self.session = requests.Session()
        self.session.verify = verify
        self._authenticate(username, password, account_id)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        response = self.session.request(method, f"{self.base_url}{path}", timeout=30, **kwargs)
        response.raise_for_status()
        return response

    def _authenticate(self, username: str, password: str, account_id: str | None) -> None:
        credentials: dict[str, Any] = {"username": username, "password": password}
        if account_id:
            credentials["accountId"] = account_id
        response = self._request("post", "/api/v3/authorize", json=credentials)
        token = extract_token(response)
        self.session.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def get(self, path: str) -> Any:
        return self._request("get", path).json()

    def post(self, path: str, payload: dict[str, Any]) -> requests.Response:
        return self._request("post", path, json=payload)

    def put(self, path: str, payload: dict[str, Any]) -> requests.Response:
        return self._request("put", path, json=payload)

    def delete(self, path: str) -> requests.Response:
        return self._request("delete", path)

    def health(self) -> Any:
        """Call a simple authenticated endpoint to prove connectivity works."""
        return self.get(HEALTH_PATH)


# --------------------------------------------------------------------------
# CLI - standalone connectivity/health check only
# --------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--auth-config", help="YAML file with connection settings (see auth.example.yaml)")
    parser.add_argument("--host", default=None, help="Overrides --auth-config / STORAGEGRID_HOST")
    parser.add_argument("--username", default=None, help="Overrides --auth-config / STORAGEGRID_USERNAME")
    parser.add_argument("--password", default=None, help="Overrides --auth-config / STORAGEGRID_PASSWORD")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification")
    parser.add_argument("--ca-bundle", default=None, help="Path to a CA bundle used to verify the certificate")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        auth_config = load_yaml(args.auth_config, default={})
        connection = resolve_connection(args, auth_config)
        if connection["verify"] is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        client = StorageGRIDClient(**connection)
        print(json.dumps(client.health(), indent=2))
    except requests.exceptions.SSLError as error:
        print(f"StorageGRID TLS verification failed: {error}", file=sys.stderr)
        print("For a lab certificate, set insecure: true in the config, or provide ca_bundle.", file=sys.stderr)
        return 1
    except requests.RequestException as error:
        print(f"StorageGRID API request failed: {error}", file=sys.stderr)
        if error.response is not None:
            print(error.response.text, file=sys.stderr)
        return 1
    except (ValueError, yaml.YAMLError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
