# Display SMB Share & File information from ONTAP

Goal:
1. Display All SMB Shares (for vserver/SVM)
2. Display top-levle Directories within Shares
3. Display NTFS permissions on path (file / directory)

## ONTAP APIs

### `curl` Authentication

`curl -siku <username>:<password> -X GET "https://mgmt_ip_address/api/storage/volumes"`

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://192.168.0.101/api/storage/volumes"
```

### ONTAP `CIFS SHARES`

#### ONTAP API Swagger example 

This can help define the parameters and review options available.

`curl -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15" -H  "accept: application/json" -H  "authorization: Basic YWRtaW46TmV0YXBwMSE="`

Replace autorization token with credentials.

#### `curl` native example

`curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15"`

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15" 
  ```

  #### GET SVM UUID

  `curl -siku admin:Netapp1! -X GET "https://cluster1/api/svm/svms?name=ntap-svm01-nas&return_records=true&return_timeout=15"`

**Output:**

  ```shell
  [root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/svm/svms?name=ntap-svm01-nas&return_records=true&return_timeout=15"
HTTP/1.1 200 OK
Date: Thu, 27 Mar 2025 17:42:32 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Dot-Ttag: 8803e80000000e27
Content-Length: 392
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin

{
  "records": [
    {
      "uuid": "52d5f766-0b2d-11f0-b971-0050569d0ad0",
      "name": "ntap-svm01-nas",
      "_links": {
        "self": {
          "href": "/api/svm/svms/52d5f766-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/svm/svms?name=ntap-svm01-nas&return_records=true&return_timeout=15"
    }
  }
```
