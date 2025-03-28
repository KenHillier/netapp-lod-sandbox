# Display Network Port Statistics

## Display Network Port Statistics with `ifstat -a`

Using the Data ONTAP 7-Mode command `ifstat -a` to collect these fields:

| Metric            | Description                     | Example Value | ONTAP |
|--------------------|---------------------------------|---------------| ----- |
| Total discards     | Total number of discarded packets | 120          | N/A |
| Discards/minute    | Average discards per minute     | 5             | N/A |
| Xon               | Number of Xon frames received   | 15            | N/A |
| Xoff              | Number of Xoff frames received  | 10            | N/A |
| Pause             | Number of pause frames received | 8             | N/A |
| CRC errors        | Number of CRC errors detected   | 2             | Maybe - port-health-monitor CRC monitor |
| Speed             | Network port speed              | 1 Gbps        | Yes |
| Duplex            | Duplex mode of the port         | Full          | Yes |
| Flowcontrol       | Flow control status             | Enabled       | Yes |
| Media state       | Current state of the media      | Up            | Yes |
| Up to downs       | Number of up-to-down transitions | 3            | Maybe - port-health-monitor Link-flapping |

N/A means `ifstat` on the node shell is needed.

## ONTAP REST CLI - private CLI passthrough example

API: /private/cli

One way would be to use the *rest_cli*

Syntax example passing a JSON data frame to the private/CLI passthrough with REST:

```shell
$ curl -ku admin:Netapp1! -X POST https://cluster1/api/private/cli -d '{ "input": "set diag; vserver config override -command \"volume show -vserver vs1\" " }'
{
  "output": "\nVserver   Volume       Aggregate    State      Type       Size  Available Used%\n--------- ------------ ------------ ---------- ---- ---------- ---------- -----\nvs1       foo          aggr         online     RW         20MB    18.76MB    1%\nvs1       foo2         aggr         online     RW         20MB    18.76MB    1%\nvs1       foo3         aggr         online     RW         20MB    18.76MB    1%\nvs1       vol1         aggr         online     RW         20MB    17.84MB    6%\nvs1       vs1_root     aggr         online     RW         20MB    17.36MB    8%\n5 entries were displayed.\n\n\n"
}
```

```shell
# Display port statistics for e0c
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X POST https://cluster1/api/private/cli -d '{ "input": "set diag; verver config override -command \"system node run -node local -command ifstat e0c\" "}'

# Display port statistics for all port on system
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X POST https://cluster1/api/private/cli -d '{ "input": "set diag; verver config override -command \"system node run -node local -command ifstat -a\" "}'

# Output for one port - e0c
[root@rhel1 netapp-lod-sandbox]#curl -siku admin:Netapp1! -X POST https://cluster1/api/private/cli -d '{ "input": "set diag; vserver config override -command \"system node run -node local -command ifstat e0c\" "}'
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 22:08:42 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Dot-Ttag: 8803e80000002726
Content-Length: 2263
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin

{
  "output": "\n\n-- interface  e0c  (1 day, 8 hours, 38 minutes, 8 seconds) --\n\nRECEIVE\n Total frames:      147k | Frames/second:       1  | Total bytes:     19749k\n Bytes/second:      168  | Total errors:        0  | Errors/minute:       0 \n Total discards:      0  | Discards/minute:     0  | Multi/broadcast:     0 \n Non-primary u/c:     0  | Errored frames:      0  | Unsupported Op:      0 \n CRC errors:          0  | Runt frames:         0  | Fragment:            0 \n Long frames:         0  | Jabber:              0  | Length errors:       0 \n Alignment errors:    0  | No buffer:           0  | Xon:                 0 \n Xoff:                0  | Jumbo:               0  | Noproto:             0 \n Error symbol:        0  | Illegal symbol:      0  | Bus overruns:        0 \n Queue drops:         0  | LRO segments:        0  | LRO bytes:           0 \n LRO6 segments:       0  | LRO6 bytes:          0  | Bad UDP cksum:       0 \n Bad UDP6 cksum:      0  | Bad TCP cksum:       0  | Bad TCP6 cksum:      0 \n Mcast v6 solicit:  940  | Lagg errors:         0  | Lacp errors:         0 \n Lacp PDU errors:     0 \nTRANSMIT\n Total frames:    64177  | Frames/second:       1  | Total bytes:     68692k\n Bytes/second:      585  | Total errors:        0  | Errors/minute:       0 \n Total discards:      0  | Queue overflow:      0  | Multi/broadcast:     0 \n Collisions:          0  | Max collisions:      0  | Single collision:    0 \n Multi collisions:    0  | Late collisions:     0  | Xon:                 0 \n Xoff:                0  | Pause:               0  | Jumbo:               0 \n Cfg Up to Downs:     0  | TSO non-TCP drop:    0  | Split hdr drop:      0 \n Timeout:             0  | TSO segments:        0  | TSO bytes:           0 \n TSO6 segments:       0  | TSO6 bytes:          0  | HW UDP cksums:    1496 \n HW UDP6 cksums:      0  | HW TCP cksums:   57336  | HW TCP6 cksums:      0 \n Mcast v6 solicit:    0  | Lagg drops:          0  | Lagg no buffer:      0 \n Lagg no entries:     0 \nDEVICE\n Mcast addresses:     3  | Rx MBuf Sz:       4096 \nLINK INFO\n Speed:            1000M | Duplex:            full | Flowcontrol:       full\n Media state:     active | Up to downs:          1 | HW assist:           6 \n\n\n\n"
}
```

API: 
/network/port
/network/port/{uuid}

### `/network/port` example
```shell
# Display all ports on node 1: cluster1-01
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/network/ethernet/ports?node.name=cluster1-01&return_records=true&return_timeout=15"
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 21:27:45 GMT
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
      "uuid": "0a34c002-0b2d-11f0-b971-0050569d0ad0",
      "name": "a0a",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/0a34c002-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    },
    {
      "uuid": "dae4c927-a771-11ef-8df6-005056b03f60",
      "name": "e0a",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae4c927-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae50aa8-a771-11ef-8df6-005056b03f60",
      "name": "e0b",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae50aa8-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae52755-a771-11ef-8df6-005056b03f60",
      "name": "e0c",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae52755-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae54190-a771-11ef-8df6-005056b03f60",
      "name": "e0d",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae54190-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae55c74-a771-11ef-8df6-005056b03f60",
      "name": "e0e",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae55c74-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae576cf-a771-11ef-8df6-005056b03f60",
      "name": "e0f",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae576cf-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "dae5917d-a771-11ef-8df6-005056b03f60",
      "name": "e0g",
      "node": {
        "name": "cluster1-01"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/ports/dae5917d-a771-11ef-8df6-005056b03f60"
        }
      }
    }
  ],
  "num_records": 8,
  "_links": {
    "self": {
      "href": "/api/network/ethernet/ports?node.name=cluster1-01&return_records=true&return_timeout=15"
    }
  }
```

### `/network/port/{uuid}` example
```shell
[root@rhel1 netapp-lod-sandbox]# curl -siku admin:Netapp1! -X GET "https://cluster1/api/network/ethernet/ports/dae52755-a771-11ef-8df6-005056b03f60?return_records=true&return_timeout=15"
HTTP/1.1 200 OK
Date: Fri, 28 Mar 2025 21:30:38 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Dot-Ttag: 8803e8000000264f
Content-Length: 1555
Content-Type: application/hal+json
Vary: Accept-Encoding,Origin

{
  "uuid": "dae52755-a771-11ef-8df6-005056b03f60",
  "name": "e0c",
  "mac_address": "00:50:56:9d:bf:28",
  "type": "physical",
  "node": {
    "uuid": "1045db6a-a771-11ef-8df6-005056b03f60",
    "name": "cluster1-01",
    "_links": {
      "self": {
        "href": "/api/cluster/nodes/1045db6a-a771-11ef-8df6-005056b03f60"
      }
    }
  },
  "broadcast_domain": {
    "uuid": "e1726de3-a771-11ef-8df6-005056b03f60",
    "name": "Default",
    "ipspace": {
      "name": "Default"
    },
    "_links": {
      "self": {
        "href": "/api/network/ethernet/broadcast-domains/e1726de3-a771-11ef-8df6-005056b03f60"
      }
    }
  },
  "enabled": true,
  "state": "up",
  "mtu": 1500,
  "speed": 1000,
  "flowcontrol_admin": "full",
  "pfc_queues_admin": [
  ],
  "reachability": "not_repairable",
  "reachable_broadcast_domains": [
    {
      "uuid": "e1726de3-a771-11ef-8df6-005056b03f60",
      "name": "Default",
      "ipspace": {
        "name": "Default"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/broadcast-domains/e1726de3-a771-11ef-8df6-005056b03f60"
        }
      }
    },
    {
      "uuid": "097d5ef8-0b2d-11f0-b971-0050569d0ad0",
      "name": "bc_data",
      "ipspace": {
        "name": "Default"
      },
      "_links": {
        "self": {
          "href": "/api/network/ethernet/broadcast-domains/097d5ef8-0b2d-11f0-b971-0050569d0ad0"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/network/ethernet/ports/dae52755-a771-11ef-8df6-005056b03f60"
    }
  }
}
```