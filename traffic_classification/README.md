# StorageGRID traffic classification

The folder has four small scripts:

- [storagegrid_auth.py](storagegrid_auth.py) — shared login and health check.
- [storagegrid_tenants.py](storagegrid_tenants.py) — create test tenants and buckets.
- [storagegrid_traffic_classification.py](storagegrid_traffic_classification.py) — list or apply traffic-classification policies.
- [storagegrid_tc_policy_yaml.py](storagegrid_tc_policy_yaml.py) — list tenant names and draft monitor-only policy YAML for later apply.

Keep each config file separate: auth, tenant data, and policy data stay in different YAML files.

## Setup

```bash
python3 -m pip install requests pyyaml
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

### List tenant accounts

```bash
python3 storagegrid_tenants.py list --auth-config auth.local.yaml
```

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

This creates a YAML draft with one monitor-only policy per tenant name, which can then be reviewed and applied with the main policy script.

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

## LabOnDemand note

These scripts are intended to be run in a StorageGRID lab environment such as the NetApp LabOnDemand training and demo environments. If you are working in a lab that already exposes the grid endpoint, the scripts here are designed to be used directly against that environment with the standard `auth.local.yaml` flow.

This is especially relevant for the StorageGRID labs used for tenant and traffic-classification exercises, including the NetApp customer-facing lab experience. If you are using this in that environment, the workflow is simply: authenticate, list or inspect tenants and policies, then generate or apply the policy YAML as needed.

## CLI overrides

You can override any auth setting on the command line: `--host`, `--username`,
`--password`, `--insecure`, and `--ca-bundle`.

Precedence is: CLI flag > `--auth-config` file > `STORAGEGRID_*` environment variable.