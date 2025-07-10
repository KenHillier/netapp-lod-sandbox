#!/bin/bash
# filepath: display_ntfs_acls.sh

# Usage: ./display_ntfs_acls.sh <cluster> <svm_name> <path>
# Example: ./display_ntfs_acls.sh 192.168.0.101 ntap-svm01-nas /autoprov_vol

CLUSTER="$1"
SVM_NAME="$2"
PATH_RAW="$3"
USER="admin"
PASS="Netapp1!"

# Get SVM UUID
SVM_UUID=$(curl -sku $USER:$PASS -X GET "https://$CLUSTER/api/svm/svms?name=$SVM_NAME&return_records=true" | jq -r '.records[0].uuid')

if [[ -z "$SVM_UUID" || "$SVM_UUID" == "null" ]]; then
  echo "Could not find SVM UUID for $SVM_NAME"
  exit 1
fi

# URL-encode the path (replace / with %2F)
PATH_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$PATH_RAW'''))")

# Get NTFS ACLs
curl -sku $USER:$PASS -X GET "https://$CLUSTER/api/protocols/file-security/permissions/$SVM_UUID/$PATH_ENC" | jq