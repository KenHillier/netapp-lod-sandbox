# Display SMB Share & File information from ONTAP

Goal:
1. Display All SMB Shares (for vserver/SVM)
2. Display top-level Directories within Shares
3. Display NTFS permissions on path (file / directory)

## ONTAP APIs

[ Base URL: /api ]
[ REST API Online Reference (Swabber): https://cluster1/docs/api/  ]

### ONTAP API Swagger

```shell
https://cluster1/api/docs
```

### `curl` Basic Authentication Example

API: /storage/volumes

`curl -siku <username>:<password> -X GET "https://mgmt_ip_address/api/storage/volumes"`

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://192.168.0.101/api/storage/volumes"
```

### ONTAP `CIFS SHARES`

API: /protocols/cifs/shares

#### ONTAP API Swagger example 

This can help define the parameters and review options available.

`curl -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15" -H  "accept: application/json" -H  "authorization: Basic YWRtaW46TmV0YXBwMSE="`

Replace autorization token with basic auth credentials.

#### `curl` native example

API: /protocols/cifs/shares - Provide svm.name to list shares

```shell
curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15"
```

**Output:**
```shell
{
  "records": [
    {
      "svm": {
        "uuid": "52d5f766-0b2d-11f0-b971-0050569d0ad0",
        "name": "ntap-svm01-nas",
        "_links": {
          "self": {
            "href": "/api/svm/svms/52d5f766-0b2d-11f0-b971-0050569d0ad0"
          }
        }
      },
      "name": "c$",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/c%24"
        }
      }
    },
      "name": "ontap_32_vol_qt01",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_vol_qt01"
        }
      }
    },
    {
      "svm": {
        "uuid": "52d5f766-0b2d-11f0-b971-0050569d0ad0",
        "name": "ntap-svm01-nas",
        "_links": {
          "self": {
            "href": "/api/svm/svms/52d5f766-0b2d-11f0-b971-0050569d0ad0"
          }
        }
      },
. . . 
```


### Display top-level directories 

API:
/storage/volumes - GET volume UUID
/storage/volumes/{volume.uuid}/files/{path} - List directories and files

#### GET Volume UUID

API: /storage/volumes

`curl -siku admin:Netapp1! -X GET "https://cluster1/api/storage/volumes?is_constituent=false&svm.name=ntap-svm01-nas&is_svm_root=false&return_records=true&return_timeout=15"`

**Output:**
```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/storage/volumes?is_constituent=false&svm.name=ntap-svm01-nas&is_svm_root=false&return_records=true&return_timeout=15"

{
  "records": [
    {
      "uuid": "a1befb05-0b2d-11f0-b971-0050569d0ad0",
      "name": "ontap_32_cifs_vol01",
      "is_svm_root": false,
      "svm": {
        "name": "ntap-svm01-nas"
      },
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    },
    {
      "uuid": "d2dd3cb3-0b2d-11f0-b971-0050569d0ad0",
      "name": "ontap_32_cifs_fg01",
      "is_svm_root": false,
      "svm": {
        "name": "ntap-svm01-nas"
      },
      "_links": {
        "self": {
          "href": "/api/storage/volumes/d2dd3cb3-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/storage/volumes?is_constituent=false&svm.name=ntap-svm01-nas&is_svm_root=false&return_records=true&return_timeout=15"
    }
  }
}
```

#### Display contents of path

API: /storage/volumes/{UUID}/files/{path}/

**Command:**
```shell
curl -siku admin:Netapp1! -X GET "https://cluster1/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01/"
```

**Output:**
```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/storage/volumes/a1befb05-0b2d-11f0-b9710050569d0ad0/files/ontap_32_vol_qt01/"
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 19:44:50 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin
Transfer-Encoding: chunked

{
  "records": [
    {
      "name": ".",
      "path": "ontap_32_vol_qt01",
      "type": "directory",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2F%2E"
        },
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2F%2E?return_metadata=true"
        }
      }
    },
    {
      "name": "..",
      "path": "ontap_32_vol_qt01",
      "type": "directory",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2F%2E%2E"
        },
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2F%2E%2E?return_metadata=true"
        }
      }
    },
    {
      "name": "ontap_32_vol_qt01_testfile",
      "path": "ontap_32_vol_qt01",
      "type": "file",
      "_links": {
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fontap_32_vol_qt01_testfile?return_metadata=true"
        }
      }
    },
    {
      "name": "dir1",
      "path": "ontap_32_vol_qt01",
      "type": "directory",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir1"
        },
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir1?return_metadata=true"
        }
      }
    },
    {
      "name": "dir2",
      "path": "ontap_32_vol_qt01",
      "type": "directory",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir2"
        },
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir2?return_metadata=true"
        }
      }
    },
    {
      "name": "dir3",
      "path": "ontap_32_vol_qt01",
      "type": "directory",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir3"
        },
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Fdir3?return_metadata=true"
        }
      }
    },
    {
      "name": "file1.txt",
      "path": "ontap_32_vol_qt01",
      "type": "file",
      "_links": {
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Ffile1%2Etxt?return_metadata=true"
        }
      }
    },
    {
      "name": "file2.txt",
      "path": "ontap_32_vol_qt01",
      "type": "file",
      "_links": {
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Ffile2%2Etxt?return_metadata=true"
        }
      }
    },
    {
      "name": "file3.txt",
      "path": "ontap_32_vol_qt01",
      "type": "file",
      "_links": {
        "metadata": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01%2Ffile3%2Etxt?return_metadata=true"
        }
      }
    }
  ],
  "num_records": 9,
  "_links": {
    "self": {
      "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0/files/ontap_32_vol_qt01/"
    }
  }

```

### Display NTFS permissions on path (file / directory)

API:
/svm/svms
/protocols/file-security/permissions/{svm.uuid}/{path}

#### GET SVM UUID

API: /svm/svms

`curl -siku admin:Netapp1! -X GET "https://cluster1/api/svm/svms?name=ntap-svm01-nas&return_records=true&return_timeout=15"`

**Output:**

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/svm/svms?name=ntap-svm01-nas&return_records=true&return_timeout=15"

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
}
```

#### GET file-security

Note: {path} needs to be encoded - /'s are %2F

**Example:**
```shell
curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/file-security/permissions/{svm.uuid}/{path}

# Check directory `dir1` in `ontap_32_vol_qt01`
curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/file-security/permissions/52df766-0b2d-11f0-b971-0050569d0ad0/%2Fontap_32_cifs_vol01%2Fontap_32_vol_qt01"
```

**Output:**
```shell
# Wrong path syntax error
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/file-security/permissions/52df766-0b2d-11f0-b971-0050569d0ad0/ontap_32_cifs_vol01/ontap_32_vol_qt01"
HTTP/1.1 404 Not Found
Date: Fri, 28 Mar 2025 19:59:27 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
Content-Length: 102
Content-Type: application/hal+json
Vary: Origin

{
  "error": {
    "message": "Unexpected argument \"ontap_32_vol_qt01\".",
    "code": "262179"
  }
}

# Check Qtree (directory) `ontap_32_vol_qt01` in `ontap_32_vol_qt01`
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/file-security/permissions/52df766-0b2d-11f0-b971-0050569d0ad0/%2Fontap_32_cifs_vol01%2Fontap_32_vol_qt01"
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 20:00:19 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Dot-Ttag: 8803e8000000251f
Content-Length: 1646
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin

{
  "svm": {
    "uuid": "52d5f766-0b2d-11f0-b971-0050569d0ad0",
    "name": "ntap-svm01-nas",
    "_links": {
      "self": {
        "href": "/api/svm/svms/52d5f766-0b2d-11f0-b971-0050569d0ad0"
      }
    }
  },
  "path": "/ontap_32_cifs_vol01/ontap_32_vol_qt01",
  "owner": "BUILTIN\\Administrators",
  "group": "BUILTIN\\Administrators",
  "control_flags": "0x8004",
  "acls": [
    {
      "user": "Everyone",
      "access": "access_allow",
      "apply_to": {
        "this_folder": true
      },
      "advanced_rights": {
        "append_data": true,
        "delete": true,
        "delete_child": true,
        "execute_file": true,
        "full_control": true,
        "read_attr": true,
        "read_data": true,
        "read_ea": true,
        "read_perm": true,
        "write_attr": true,
        "write_data": true,
        "write_ea": true,
        "write_owner": true,
        "synchronize": true,
        "write_perm": true
      },
      "inherited": true,
      "access_control": "file_directory"
    },
    {
      "user": "Everyone",
      "access": "access_allow",
      "apply_to": {
        "files": true,
        "sub_folders": true
      },
      "inherited": true,
      "access_control": "file_directory"
    }
  ],
  "inode": 97,
  "security_style": "ntfs",
  "effective_style": "ntfs",
  "dos_attributes": "10",
  "text_dos_attr": "----D---",
  "user_id": "0",
  "group_id": "0",
  "mode_bits": 777,
  "text_mode_bits": "rwxrwxrwx",
  "_links": {
    "self": {
      "href": "/api/protocols/file-security/permissions/52d5f766-0b2d-11f0-b971-0050569d0ad0/%2Fontap_32_cifs_vol01%2Fontap_32_vol_qt01"
    }
  }
}
```

```shell
# Check directory `dir1` in `ontap_32_vol_qt01`
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/file-security/permissions/52d5f766-0b2d-11f0-b971-0050569d0ad0/%2Fontap_32_cifs_vol01%2Fontap_32_vol_qt01%2Fdir1"
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 20:01:30 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Dot-Ttag: 8803e80000002520
Content-Length: 1661
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin

{
  "svm": {
    "uuid": "52d5f766-0b2d-11f0-b971-0050569d0ad0",
    "name": "ntap-svm01-nas",
    "_links": {
      "self": {
        "href": "/api/svm/svms/52d5f766-0b2d-11f0-b971-0050569d0ad0"
      }
    }
  },
  "path": "/ontap_32_cifs_vol01/ontap_32_vol_qt01/dir1",
  "owner": "DEMO\\na_ad_admin_user",
  "group": "DEMO\\Domain Users",
  "control_flags": "0x8004",
  "acls": [
    {
      "user": "Everyone",
      "access": "access_allow",
      "apply_to": {
        "this_folder": true
      },
      "advanced_rights": {
        "append_data": true,
        "delete": true,
        "delete_child": true,
        "execute_file": true,
        "full_control": true,
        "read_attr": true,
        "read_data": true,
        "read_ea": true,
        "read_perm": true,
        "write_attr": true,
        "write_data": true,
        "write_ea": true,
        "write_owner": true,
        "synchronize": true,
        "write_perm": true
      },
      "inherited": true,
      "access_control": "file_directory"
    },
    {
      "user": "Everyone",
      "access": "access_allow",
      "apply_to": {
        "files": true,
        "sub_folders": true
      },
      "inherited": true,
      "access_control": "file_directory"
    }
  ],
  "inode": 109,
  "security_style": "ntfs",
  "effective_style": "ntfs",
  "dos_attributes": "10",
  "text_dos_attr": "----D---",
  "user_id": "65534",
  "group_id": "65534",
  "mode_bits": 777,
  "text_mode_bits": "rwxrwxrwx",
  "_links": {
    "self": {
      "href": "/api/protocols/file-security/permissions/52d5f766-0b2d-11f0-b971-0050569d0ad0/%2Fontap_32_cifs_vol01%2Fontap_32_vol_qt01%2Fdir1"
    }
  }
}
```