# `curl` examples

### `curl` Authentication

`curl -siku <username>:<password> -X GET "https://mgmt_ip_address/api/storage/volumes"`

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://192.168.0.101/api/storage/volumes"
HTTP/1.1 200 OK
Date: Thu, 27 Mar 2025 17:21:54 GMT
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
      "uuid": "3f493fb5-0b2d-11f0-b971-0050569d0ad0",
      "name": "cluster1_ad_root",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/3f493fb5-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    },
    {
      "uuid": "52f2d63f-0b2d-11f0-b38f-0050569d0c17",
      "name": "ntap_svm01_nas_root",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/52f2d63f-0b2d-11f0-b38f-0050569d0c17"
        }
      }
    },
    {
      "uuid": "58f53b33-0b2d-11f0-b971-0050569d0ad0",
      "name": "ntap_svm02_san_root",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/58f53b33-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    },
    {
      "uuid": "a1befb05-0b2d-11f0-b971-0050569d0ad0",
      "name": "ontap_32_cifs_vol01",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/a1befb05-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    },
    {
      "uuid": "d2dd3cb3-0b2d-11f0-b971-0050569d0ad0",
      "name": "ontap_32_cifs_fg01",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/d2dd3cb3-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    }
  ],
  "num_records": 5,
  "_links": {
    "self": {
      "href": "/api/storage/volumes"
    }
  }
```

### ONTAP `CIFS SHARES`

#### Get swagger example to help define parameters

`curl -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15" -H  "accept: application/json" -H  "authorization: Basic YWRtaW46TmV0YXBwMSE="`

#### `curl` native example

`curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15"`

```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15"
HTTP/1.1 200 OK
Date: Thu, 27 Mar 2025 17:30:11 GMT
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
      "name": "ipc$",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ipc%24"
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
      "name": "ontap_32_fg_qt01",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_fg_qt01"
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
      "name": "ontap_32_fg_qt02",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_fg_qt02"
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
      "name": "ontap_32_fg_qt03",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_fg_qt03"
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
      "name": "ontap_32_fg_qt04",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_fg_qt04"
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
      "name": "ontap_32_fg_qt05",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_fg_qt05"
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
      "name": "ontap_32_vol_qt02",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_vol_qt02"
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
      "name": "ontap_32_vol_qt03",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_vol_qt03"
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
      "name": "ontap_32_vol_qt04",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_vol_qt04"
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
      "name": "ontap_32_vol_qt05",
      "_links": {
        "self": {
          "href": "/api/protocols/cifs/shares/52d5f766-0b2d-11f0-b971-0050569d0ad0/ontap_32_vol_qt05"
        }
      }
    }
  ],
  "num_records": 12,
  "_links": {
    "self": {
      "href": "/api/protocols/cifs/shares?svm.name=ntap-svm01-nas&return_records=true&return_timeout=15"
    }
  }
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
