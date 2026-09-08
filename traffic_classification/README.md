# StorageGRID traffic classification

The folder has four small scripts:

- [storagegrid_auth.py](storagegrid_auth.py) — shared login and health check.
- [storagegrid_tenants.py](storagegrid_tenants.py) — create test tenants and buckets.
- [storagegrid_traffic_classification.py](storagegrid_traffic_classification.py) — list or apply traffic-classification policies.
- [storagegrid_tc_policy_yaml.py](storagegrid_tc_policy_yaml.py) — list tenant names and draft monitor-only policy YAML for later apply.

Keep each config file separate: auth, tenant data, and policy data stay in different YAML files.

The scripts target the StorageGRID v4 Grid Management and Tenant Management
APIs, including authentication, tenant accounts, buckets, and traffic-classification
policies. StorageGRID 12.x or newer is required.

## Setup

Requires Python 3.9 or newer. Install the runtime dependencies with:

```bash
python3 -m pip install requests PyYAML urllib3
cp auth.example.yaml auth.local.yaml
cp tenants.example.yaml tenants.local.yaml
cp policies.example.yaml policies.local.yaml
```

Edit `auth.local.yaml` with your grid's host/username. Edit
`tenants.local.yaml` with the test tenants/buckets to create. Edit
`policies.local.yaml` with the policies to apply (see the comments in each
file). All `*.local.yaml` files are gitignored.

Set the password via environment variable, not the config file:

```bash
export STORAGEGRID_PASSWORD='...'
```

Note: If no password is provided by any other means, the user will be prompted for the password.

## Commands

### Check auth and connectivity

```bash
python3 storagegrid_auth.py --auth-config auth.local.yaml
```

### Create test tenants and buckets

```bash
python3 storagegrid_tenants.py apply \
  --auth-config auth.local.yaml --tenants-config tenants.local.yaml
```

### Clean up listed tenants

Use a tenant YAML file containing only the accounts to remove. Preview the
deletions with `--dry-run`, or omit it to delete the listed accounts.

```bash
python3 storagegrid_tenants.py cleanup \
  --auth-config auth.local.yaml --tenants-config tenants.cleanup.yaml --dry-run
python3 storagegrid_tenants.py cleanup \
  --auth-config auth.local.yaml --tenants-config tenants.cleanup.yaml
```

### List tenant accounts

```bash
python3 storagegrid_tenants.py list --auth-config auth.local.yaml
```

Account listing requests ask for the maximum page size of 500 and follow the
StorageGRID pagination marker, so grids with more than 500 tenant accounts are
included in the result.

### List traffic-classification policies

This prints the raw StorageGRID API JSON response:

```bash
python3 storagegrid_traffic_classification.py list --auth-config auth.local.yaml
```

Add `--summary` to print a shorter cleaned summary after the raw JSON:

```bash
python3 storagegrid_traffic_classification.py list --auth-config auth.local.yaml --summary
```

A policy name does not guarantee the API includes an ingress or egress matcher. The raw JSON shows what is actually configured on the grid.

### Generate monitor-only YAML from current tenants

```bash
python3 storagegrid_tc_policy_yaml.py list --auth-config auth.local.yaml
python3 storagegrid_tc_policy_yaml.py template \
  --auth-config auth.local.yaml --output policies.monitor.yaml
```

This creates one monitor-only policy per tenant. Review the YAML before applying it.

Generated policies use `TC Monitor <account ID>` as the policy name, the tenant
account ID as the `tenant` matcher, and the tenant name as the description.
Policy names are limited to 32 characters and descriptions to 128 characters;
invalid hand-written entries are reported individually and do not stop later
policies from being applied.

### Create or update policies

```bash
python3 storagegrid_traffic_classification.py apply \
  --auth-config auth.local.yaml --policies-config policies.local.yaml
```

Add `--summary` to show the compact policy recap after the raw API response:

```bash
python3 storagegrid_traffic_classification.py apply \
  --auth-config auth.local.yaml --policies-config policies.local.yaml --summary
```

### Clean up listed policies

Use a policy YAML file containing only the policies to remove. Preview the
deletions with `--dry-run`, or omit it to delete the listed policies.

```bash
python3 storagegrid_traffic_classification.py cleanup \
  --auth-config auth.local.yaml --policies-config policies.cleanup.yaml --dry-run
python3 storagegrid_traffic_classification.py cleanup \
  --auth-config auth.local.yaml --policies-config policies.cleanup.yaml
```

## Config file reference

`auth.local.yaml`:

```yaml
host: 192.168.0.80
username: root
insecure: true          # self-signed lab certs
# ca_bundle: /path/to/storagegrid-ca.pem
```

`tenants.local.yaml`:

```yaml
- name: appid_001              # tenant name is also the app ID
  password: Netapp1!Tenant     # reset each run
  buckets:
    - appid-001-data           # bucket name
```

`policies.local.yaml`:

```yaml
# Omit "limit" for monitor-only policies.
- name: monitor-tenant-appid-001
  tenant_name: appid_001

- name: ingest-limit
  description: Limit ingest bandwidth for my-bucket
  bucket: my-bucket
  limit: 10485760
  limit_type: aggregateBandwidthIn
```

Omit all matcher keys (`bucket`/`tenant_name`/`tenant`/`ip`) to match the
whole grid.

`limit_type` is one of: `aggregateBandwidthIn`, `aggregateBandwidthOut`,
`perRequestBandwidthIn`, `perRequestBandwidthOut`, `concurrentReadRequests`,
`concurrentWriteRequests`.

For full control, use the raw API schema with `matchers` and `limits` keys. See
[policies.example.yaml](policies.example.yaml).

## LabOnDemand

These scripts are intended for StorageGRID lab environments, including NetApp
LabOnDemand. Use the standard `auth.local.yaml` workflow to authenticate, list
tenants or policies, generate policy YAML, and apply it.

- [Lab environment](https://labondemand.netapp.com/node/1523)
- [Customer lab](https://labondemand.netapp.com/lab/gsstg-hol)

## CLI overrides

You can override any auth setting on the command line: `--host`, `--username`,
`--password`, `--insecure`, and `--ca-bundle`.

Precedence is: CLI flag > `--auth-config` file > `STORAGEGRID_*` environment variable.

## Changelog

- Added StorageGRID v4 support for 12.x and newer.
- Added paginated tenant account listing.
- Generated policies now use tenant account IDs.
- Added config-based cleanup with `--dry-run` for tenants and policies.