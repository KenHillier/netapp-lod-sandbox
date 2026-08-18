#!/usr/bin/env python3
"""List and manage StorageGRID traffic classification policies."""

import argparse
import json
import os
import sys
from typing import Any

import requests
import urllib3


HEALTH_PATH = "/api/v3/grid/config/product-version"
POLICIES_PATH = "/api/v3/grid/config/traffic-classes"


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


class StorageGRIDClient:
    def __init__(self, host: str, username: str, password: str, verify: bool = True):
        self.base_url = normalize_host(host)
        self.session = requests.Session()
        self.session.verify = verify
        response = self.session.post(
            f"{self.base_url}/api/v3/authorize",
            json={"username": username, "password": password},
            timeout=30,
        )
        response.raise_for_status()
        token = extract_token(response)
        self.session.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def list_policies(self) -> Any:
        response = self.session.get(f"{self.base_url}{POLICIES_PATH}", timeout=30)
        response.raise_for_status()
        return response.json()

    def health(self) -> Any:
        response = self.session.get(f"{self.base_url}{HEALTH_PATH}", timeout=30)
        response.raise_for_status()
        return response.json()

    def set_policy(self, policy: dict[str, Any]) -> Any:
        policies = self.list_policies()
        records = policies.get("records", policies) if isinstance(policies, dict) else policies
        existing = next(
            (item for item in records if item.get("name") == policy.get("name")), None
        )

        if existing and existing.get("id"):
            url = f"{self.base_url}{POLICIES_PATH}/{existing['id']}"
            response = self.session.put(url, json=policy, timeout=30)
        else:
            response = self.session.post(
                f"{self.base_url}{POLICIES_PATH}", json=policy, timeout=30
            )
        response.raise_for_status()
        return response.json() if response.content else {"status": response.status_code}


def build_policy(args: argparse.Namespace) -> dict[str, Any]:
    matchers = {}
    if args.bucket:
        matchers["bucket"] = args.bucket
    if args.tenant:
        matchers["tenant"] = args.tenant
    if args.ip:
        matchers["ip"] = args.ip

    policy: dict[str, Any] = {"name": args.name, "matchers": matchers}
    if args.description:
        policy["description"] = args.description
    if args.limit:
        policy["limits"] = {"bandwidth": args.limit}
    return policy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("health", "list", "set"))
    parser.add_argument("--host", default=os.getenv("STORAGEGRID_HOST"), required=not os.getenv("STORAGEGRID_HOST"))
    parser.add_argument("--username", default=os.getenv("STORAGEGRID_USERNAME"), required=not os.getenv("STORAGEGRID_USERNAME"))
    parser.add_argument("--password", default=os.getenv("STORAGEGRID_PASSWORD"), required=not os.getenv("STORAGEGRID_PASSWORD"))
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification")
    parser.add_argument(
        "--ca-bundle",
        default=os.getenv("STORAGEGRID_CA_BUNDLE"),
        help="Path to a CA bundle used to verify the StorageGRID certificate",
    )
    parser.add_argument("--name", help="Policy name (required for set)")
    parser.add_argument("--description")
    parser.add_argument("--bucket", help="Bucket name matcher")
    parser.add_argument("--tenant", help="Tenant account ID matcher")
    parser.add_argument("--ip", help="Client IP or CIDR matcher")
    parser.add_argument("--limit", type=int, help="Bandwidth limit in bytes per second")
    args = parser.parse_args()
    if args.command == "set" and not args.name:
        parser.error("set requires --name")
    return args


def main() -> int:
    args = parse_args()
    try:
        verify = False if args.insecure else (args.ca_bundle or True)
        if args.insecure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        client = StorageGRIDClient(args.host, args.username, args.password, verify)
        if args.command == "health":
            result = client.health()
        elif args.command == "list":
            result = client.list_policies()
        else:
            result = client.set_policy(build_policy(args))
        print(json.dumps(result, indent=2))
    except requests.exceptions.SSLError as error:
        print(f"StorageGRID TLS verification failed: {error}", file=sys.stderr)
        print("For a lab certificate, retry with --insecure; preferably use --ca-bundle /path/to/ca.pem.", file=sys.stderr)
        return 1
    except requests.RequestException as error:
        print(f"StorageGRID API request failed: {error}", file=sys.stderr)
        if error.response is not None:
            print(error.response.text, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())