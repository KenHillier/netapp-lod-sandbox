# Display Network Port Statistics with `ifstat -a`

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


