# StorageGRID traffic classification

This example authenticates to the StorageGRID Grid Management API, verifies the session with a health call, and lists or creates/updates a traffic classification policy.

## Requirements

```bash
python3 -m pip install requests
```

Set credentials without putting them in the command history:

```bash
export STORAGEGRID_HOST="https://admin-node.example.com"
export STORAGEGRID_USERNAME="grid-admin"
export STORAGEGRID_PASSWORD="change-me"
```

Verify authentication with a simple API call:

```bash
python3 storagegrid_traffic_classification.py health
```

List traffic classification policies:

```bash
python3 storagegrid_traffic_classification.py list
```

For a lab StorageGRID using a self-signed certificate, disable verification explicitly:

```bash
python3 storagegrid_traffic_classification.py list --insecure
```

For normal use, export the StorageGRID CA certificate and verify it instead:

```bash
export STORAGEGRID_CA_BUNDLE="/path/to/storagegrid-ca.pem"
python3 storagegrid_traffic_classification.py list
```

Create a policy, or update the existing policy with the same name:

```bash
python3 storagegrid_traffic_classification.py set \
  --name ingest-limit \
  --description "Limit ingest traffic" \
  --bucket my-bucket \
  --limit 10485760
```

Use `--tenant`, `--ip`, or a combination of matchers as needed. `--limit` is bytes per second. Use `--insecure` only for a lab with a self-signed certificate.

The exact accepted matcher and limit combinations depend on the StorageGRID release. The script prints the API response, which makes it useful as a starting point for adding release-specific fields.