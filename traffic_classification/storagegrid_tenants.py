#!/usr/bin/env python3
"""Create test tenants and buckets on StorageGRID.

Usage:
    storagegrid_tenants.py list --auth-config auth.local.yaml
    storagegrid_tenants.py apply --auth-config auth.local.yaml --tenants-config tenants.local.yaml
"""

import argparse
import json
import sys
from typing import Any

import requests
import urllib3
import yaml

from storagegrid_auth import StorageGRIDClient, load_yaml, resolve_connection


ACCOUNTS_PATH = "/api/v3/grid/accounts"
CONTAINERS_PATH = "/api/v3/org/containers"
DEFAULT_REGION = "us-east-1"


# --------------------------------------------------------------------------
# Tenant / bucket API calls
# --------------------------------------------------------------------------

def list_tenants(client: StorageGRIDClient) -> Any:
    return client.get(ACCOUNTS_PATH)


def find_tenant(client: StorageGRIDClient, name: str) -> dict[str, Any] | None:
    accounts = list_tenants(client).get("data", [])
    matches = [account for account in accounts if account.get("name") == name]
    if len(matches) > 1:
        raise ValueError(f"Multiple tenant accounts are already named '{name}'; rename or remove the duplicates")
    return matches[0] if matches else None


def ensure_tenant(client: StorageGRIDClient, name: str, password: str | None) -> dict[str, Any]:
    """Create the tenant if missing. Resets the root password every run when one is provided."""
    account = find_tenant(client, name)
    if account is None:
        response = client.post(ACCOUNTS_PATH, {"name": name, "capabilities": ["s3", "management"]})
        account = response.json()["data"]
    if password:
        client.post(f"{ACCOUNTS_PATH}/{account['id']}/change-password", {"password": password})
    return account


def ensure_bucket(tenant_client: StorageGRIDClient, bucket_name: str, region: str = DEFAULT_REGION) -> dict[str, Any]:
    existing = tenant_client.get(CONTAINERS_PATH).get("data", [])
    if any(bucket.get("name") == bucket_name for bucket in existing):
        return {"name": bucket_name, "status": "already exists"}
    response = tenant_client.post(CONTAINERS_PATH, {"name": bucket_name, "region": region})
    return response.json()["data"]


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_apply(client: StorageGRIDClient, connection: dict[str, Any], tenants: list[dict[str, Any]]) -> list[Any]:
    if not tenants:
        raise ValueError("No tenants defined. Point --tenants-config at a YAML file with a list of tenants.")

    results = []
    for tenant in tenants:
        if "name" not in tenant:
            raise ValueError("Each tenant in the config file must have a 'name'")

        buckets = tenant.get("buckets", [])
        password = tenant.get("password")
        if buckets and not password:
            raise ValueError(f"Tenant '{tenant['name']}' defines buckets but no 'password' was provided")

        account = ensure_tenant(client, tenant["name"], password)
        bucket_results = []
        if buckets:
            tenant_client = StorageGRIDClient(
                host=connection["host"],
                username="root",
                password=password,
                verify=connection["verify"],
                account_id=account["id"],
            )
            bucket_results = [ensure_bucket(tenant_client, bucket) for bucket in buckets]

        results.append({"tenant": account, "buckets": bucket_results})
    return results


# --------------------------------------------------------------------------
# Summary output (opt-in recap alongside the raw JSON)
# --------------------------------------------------------------------------

def summarize_tenant(record: dict[str, Any]) -> str:
    account = record.get("tenant", record)
    line = f"{account.get('name', '?')} ({account.get('id', '?')})"
    if "buckets" in record:
        names = ", ".join(bucket.get("name", "?") for bucket in record["buckets"]) or "none"
        line += f" | buckets: {names}"
    return line


def print_summary(result: Any) -> None:
    records = result.get("data", []) if isinstance(result, dict) else result
    print("--- summary ---")
    for record in records:
        print(summarize_tenant(record))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("list", "apply"))
    parser.add_argument("--auth-config", help="YAML file with connection settings (see auth.example.yaml)")
    parser.add_argument("--tenants-config", help="YAML file with a list of tenants (see tenants.example.yaml), required for apply")
    parser.add_argument("--host", default=None, help="Overrides --auth-config / STORAGEGRID_HOST")
    parser.add_argument("--username", default=None, help="Overrides --auth-config / STORAGEGRID_USERNAME")
    parser.add_argument("--password", default=None, help="Overrides --auth-config / STORAGEGRID_PASSWORD")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification")
    parser.add_argument("--ca-bundle", default=None, help="Path to a CA bundle used to verify the certificate")
    parser.add_argument("--summary", action="store_true", help="Also print a short recap after the raw JSON output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        auth_config = load_yaml(args.auth_config, default={})
        connection = resolve_connection(args, auth_config)
        if connection["verify"] is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        client = StorageGRIDClient(**connection)

        if args.command == "list":
            result = list_tenants(client)
        else:
            tenants = load_yaml(args.tenants_config, default=[])
            result = cmd_apply(client, connection, tenants)

        print(json.dumps(result, indent=2))
        if args.summary:
            print_summary(result)
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
