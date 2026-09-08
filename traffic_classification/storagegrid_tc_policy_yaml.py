#!/usr/bin/env python3
"""List tenant names or draft monitor-only policy YAML for traffic classification.

Examples:
    python3 storagegrid_tc_policy_yaml.py list --auth-config auth.local.yaml
    python3 storagegrid_tc_policy_yaml.py template --auth-config auth.local.yaml --output policies.monitor.yaml
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import requests
import urllib3
import yaml

from storagegrid_auth import StorageGRIDClient, load_yaml, resolve_connection


ACCOUNTS_PATH = "/api/v4/grid/accounts"


def list_tenants(client: StorageGRIDClient) -> list[dict[str, str]]:
    accounts = client.get_paginated(ACCOUNTS_PATH).get("data", [])
    return sorted(
        [
            {"id": account["id"], "name": account["name"]}
            for account in accounts
            if isinstance(account, dict) and account.get("id") and account.get("name")
        ],
        key=lambda account: account["name"],
    )


def build_monitor_policy_yaml(tenants: list[dict[str, str]]) -> list[dict[str, str]]:
    policies: list[dict[str, str]] = []
    for tenant in tenants:
        policies.append(
            {
                "name": f"TC Monitor {tenant['id']}",
                "description": tenant["name"],
                "tenant": tenant["id"],
            }
        )
    return policies


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("list", "template"), help="List tenant names or generate monitor-only YAML policy stubs")
    parser.add_argument("--auth-config", help="YAML file with connection settings (see auth.example.yaml)")
    parser.add_argument("--host", default=None, help="Overrides --auth-config / STORAGEGRID_HOST")
    parser.add_argument("--username", default=None, help="Overrides --auth-config / STORAGEGRID_USERNAME")
    parser.add_argument("--password", default=None, help="Overrides --auth-config / STORAGEGRID_PASSWORD")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification")
    parser.add_argument("--ca-bundle", default=None, help="Path to a CA bundle used to verify the certificate")
    parser.add_argument("--output", help="Write generated YAML to this file instead of stdout")
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
            tenants = list_tenants(client)
            for tenant in tenants:
                print(tenant["name"])
            return 0

        tenants = list_tenants(client)
        policies = build_monitor_policy_yaml(tenants)
        rendered = yaml.safe_dump(policies, sort_keys=False, default_flow_style=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(rendered)
            print(f"Wrote {len(policies)} monitor-only policy entries to {args.output}")
        else:
            print(rendered, end="")
        return 0

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
