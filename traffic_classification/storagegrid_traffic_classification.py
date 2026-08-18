#!/usr/bin/env python3
"""List and apply StorageGRID traffic classification policies.

Usage:
    storagegrid_traffic_classification.py list  --auth-config auth.local.yaml
    storagegrid_traffic_classification.py apply --auth-config auth.local.yaml --policies-config policies.local.yaml

Run storagegrid_auth.py first to verify connectivity (see its --help).
See auth.example.yaml and policies.example.yaml for the input file formats.
"""

import argparse
import json
import sys
from typing import Any

import requests
import urllib3
import yaml

from storagegrid_auth import StorageGRIDClient, load_yaml, resolve_connection


POLICIES_PATH = "/api/v3/grid/traffic-classes/policies"
ACCOUNTS_PATH = "/api/v3/grid/accounts"

LIMIT_TYPES = (
    "aggregateBandwidthIn",
    "aggregateBandwidthOut",
    "perRequestBandwidthIn",
    "perRequestBandwidthOut",
    "concurrentReadRequests",
    "concurrentWriteRequests",
)


# --------------------------------------------------------------------------
# Policy API calls
# --------------------------------------------------------------------------

def list_policies(client: StorageGRIDClient) -> Any:
    return client.get(POLICIES_PATH)


def find_policy_id(client: StorageGRIDClient, name: str) -> str | None:
    records = list_policies(client).get("data", [])
    return next((item["id"] for item in records if item.get("name") == name), None)


def apply_policy(client: StorageGRIDClient, payload: dict[str, Any]) -> Any:
    """Create the policy, or update it in place if a policy with the same name exists."""
    existing_id = find_policy_id(client, payload["name"])
    if existing_id:
        response = client.put(f"{POLICIES_PATH}/{existing_id}", payload)
    else:
        response = client.post(POLICIES_PATH, payload)
    return response.json() if response.content else {"status": response.status_code}


def resolve_tenant_id(client: StorageGRIDClient, tenant_name: str) -> str:
    """Look up a tenant account id by its name (tenant names double as application IDs)."""
    accounts = client.get(ACCOUNTS_PATH).get("data", [])
    matches = [account["id"] for account in accounts if account.get("name") == tenant_name]
    if not matches:
        raise ValueError(f"No tenant account named '{tenant_name}' was found")
    if len(matches) > 1:
        raise ValueError(f"Multiple tenant accounts are named '{tenant_name}'; use 'tenant' with the exact account id instead")
    return matches[0]


# --------------------------------------------------------------------------
# Policy payload construction
# --------------------------------------------------------------------------

def build_matcher(match_type: str, value: Any) -> dict[str, Any]:
    members = value if isinstance(value, list) else [value]
    return {"type": match_type, "inverse": False, "members": members}


def build_policy_payload(policy: dict[str, Any]) -> dict[str, Any]:
    """Translate a policy definition from the config file into the StorageGRID API schema.

    Supports simplified keys (bucket/tenant/ip/limit/limit_type) or the raw
    matchers/limits arrays for full control. Omit "limit" for a monitor-only
    policy (metrics only, no enforcement). Omit all matcher keys for a
    grid-wide policy.
    """
    if "name" not in policy:
        raise ValueError("Each policy in the config file must have a 'name'")

    if "matchers" in policy or "limits" in policy:
        payload: dict[str, Any] = {"name": policy["name"], "matchers": policy.get("matchers", [])}
        if "description" in policy:
            payload["description"] = policy["description"]
        if "limits" in policy:
            payload["limits"] = policy["limits"]
        return payload

    matchers = []
    if policy.get("bucket"):
        matchers.append(build_matcher("bucket", policy["bucket"]))
    if policy.get("tenant"):
        matchers.append(build_matcher("tenant", policy["tenant"]))
    if policy.get("ip"):
        matchers.append(build_matcher("cidr", policy["ip"]))

    payload = {"name": policy["name"], "matchers": matchers}
    if policy.get("description"):
        payload["description"] = policy["description"]
    if policy.get("limit") is not None:
        limit_type = policy.get("limit_type", "aggregateBandwidthIn")
        if limit_type not in LIMIT_TYPES:
            raise ValueError(f"Unsupported limit_type '{limit_type}' for policy '{policy['name']}'")
        payload["limits"] = [{"type": limit_type, "value": policy["limit"]}]
    return payload


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_apply(client: StorageGRIDClient, policies: list[dict[str, Any]]) -> list[Any]:
    if not policies:
        raise ValueError("No policies defined. Point --policies-config at a YAML file with a list of policies.")
    return [apply_policy(client, build_policy_payload(resolve_tenant_name(client, policy))) for policy in policies]


def resolve_tenant_name(client: StorageGRIDClient, policy: dict[str, Any]) -> dict[str, Any]:
    """Replace a policy's 'tenant_name' (application ID) with the matching 'tenant' account id."""
    if "tenant_name" not in policy:
        return policy
    policy = dict(policy)
    policy["tenant"] = resolve_tenant_id(client, policy.pop("tenant_name"))
    return policy


# --------------------------------------------------------------------------
# Summary output (opt-in recap alongside the raw JSON)
# --------------------------------------------------------------------------

def summarize_policy(record: dict[str, Any]) -> str:
    parts = [record.get("name", "?")]
    matchers = record.get("matchers")
    if matchers:
        parts.append("matchers=" + ",".join(f"{m.get('type')}:{','.join(m.get('members', []))}" for m in matchers))
    elif matchers is not None:
        parts.append("matchers=grid-wide")
    limits = record.get("limits")
    if limits:
        parts.append("limits=" + ",".join(f"{l.get('type')}={l.get('value')}" for l in limits))
    elif limits is not None:
        parts.append("monitor-only")
    return " | ".join(parts)


def print_summary(result: Any) -> None:
    if isinstance(result, dict):
        records = result.get("data", [])
    elif isinstance(result, list):
        records = [item["data"] for item in result if isinstance(item, dict) and "data" in item]
    else:
        records = []
    print("--- summary ---")
    for record in records:
        print(summarize_policy(record))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("list", "apply"))
    parser.add_argument("--auth-config", help="YAML file with connection settings (see auth.example.yaml)")
    parser.add_argument("--policies-config", help="YAML file with a list of policies (see policies.example.yaml), required for apply")
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
            result = list_policies(client)
        else:
            policies = load_yaml(args.policies_config, default=[])
            result = cmd_apply(client, policies)

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