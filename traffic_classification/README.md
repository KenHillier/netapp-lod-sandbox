# StorageGRID traffic classification

Three scripts:

- [storagegrid_auth.py](storagegrid_auth.py) — foundation module. Authenticates
  and runs a basic health check. Import `StorageGRIDClient`, `load_yaml`, and
  `resolve_connection` from here to build other StorageGRID scripts.
- [storagegrid_tenants.py](storagegrid_tenants.py) — creates test tenants and
  buckets. A tenant's `name` doubles as an application ID (e.g. `appid_001`).
- [storagegrid_traffic_classification.py](storagegrid_traffic_classification.py) —
  imports the foundation module and focuses only on listing/applying traffic
  classification policies. Policies can reference a tenant by `tenant_name`
  (the application ID) instead of its StorageGRID account id.

Connection settings, tenant/bucket definitions, and policy definitions each
live in their own config file, so credentials never mix with test data.

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

Verify connectivity and authentication:

```bash
python3 storagegrid_auth.py --auth-config auth.local.yaml
```

Create the test tenants and buckets defined in `tenants.local.yaml` (creates
if missing; resets the tenant root password and adds any missing buckets if
they already exist):

```bash
python3 storagegrid_tenants.py apply \
  --auth-config auth.local.yaml --tenants-config tenants.local.yaml
```

List existing tenant accounts:

```bash
python3 storagegrid_tenants.py list --auth-config auth.local.yaml
```

List existing traffic classification policies:

```bash
python3 storagegrid_traffic_classification.py list --auth-config auth.local.yaml
```

Create or update every policy defined in `policies.local.yaml` (matched and
updated in place by `name`):

```bash
python3 storagegrid_traffic_classification.py apply \
  --auth-config auth.local.yaml --policies-config policies.local.yaml
```

## Config file reference

`auth.local.yaml`:

```yaml
host: 192.168.0.80
username: root
insecure: true          # only for a lab grid with a self-signed certificate
# ca_bundle: /path/to/storagegrid-ca.pem
```

`tenants.local.yaml`:

```yaml
- name: appid_001              # tenant name doubles as the application ID
  password: Netapp1!Tenant     # sets/resets the tenant root password each run
  buckets:
    - appid-001-data           # bucket names follow S3 naming rules (hyphens, not underscores)
```

`policies.local.yaml`:

```yaml
# Monitor-only: omit "limit" for metrics without enforcement.
- name: monitor-tenant-appid-001
  tenant_name: appid_001       # resolved to the tenant's account id at apply time

# With a limit:
- name: ingest-limit
  description: Limit ingest bandwidth for my-bucket
  bucket: my-bucket            # or: tenant_name: <name>, tenant: <id>, or: ip: <cidr>
  limit: 10485760              # bytes/sec (or a count, for concurrency limit types)
  limit_type: aggregateBandwidthIn
```

Omit all matcher keys (`bucket`/`tenant_name`/`tenant`/`ip`) to match the
whole grid.

`limit_type` is one of: `aggregateBandwidthIn`, `aggregateBandwidthOut`,
`perRequestBandwidthIn`, `perRequestBandwidthOut`, `concurrentReadRequests`,
`concurrentWriteRequests`. Bandwidth types are bytes/sec; concurrency types are
a request count.

For full control (multiple matchers/limits per policy, or a raw tenant
account id), use the raw API schema directly with `matchers`/`limits` keys
instead of the simplified ones — see the commented example in
[policies.example.yaml](policies.example.yaml).

## CLI overrides

Any connection setting can be overridden on the command line instead of (or
in addition to) `auth.local.yaml`: `--host`, `--username`, `--password`,
`--insecure`, `--ca-bundle`. Precedence is CLI flag > `--auth-config` file >
`STORAGEGRID_*` environment variable.