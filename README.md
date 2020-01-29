# notiOne Device Tracker
This device tracker uses unofficial API to get data from https://web.notione.com/index.html

## Configuration options
| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `username` | `string` | `True` | - | Username from notiOne |
| `password` | `string` | `True` | - | Password from notiOne |
| `scan_interval` | `int` | `False` | 300 | Scan interval |

## Usage:
Add to configuration.yaml:

```
device_tracker:
  - platform: notione
    username: [USERNAME FROM NOTIONE]
    password: [PASSWORD FROM NOTIONE]
```
