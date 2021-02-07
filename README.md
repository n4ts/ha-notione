# notiOne Device Tracker
[![GitHub Release][releases-shield]][releases]
[![GitHub All Releases][downloads-total-shield]][releases]
[![Hacs Badge][hacs-badge]][hacs-badge-url]
[![PayPal_Me][paypal-me-shield]][paypal-me]

This device tracker uses unofficial API to get data from https://web.notione.com/index.html

## Configuration options
| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `username` | `string` | `True` | - | Username from notiOne |
| `password` | `string` | `True` | - | Password from notiOne |
| `scan_interval` | `int` | `False` | 300 | Scan interval |

## View
![Screenshot](https://github.com/n4ts/ha-notione/blob/master/images/notione.png?raw=true)

## Usage:
Add to configuration.yaml:

```
device_tracker:
  - platform: notione
    username: [USERNAME FROM NOTIONE]
    password: [PASSWORD FROM NOTIONE]
```

## Installation

Download [*device_tracker.py*](https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/device_tracker.py), [*system_health.py*](https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/system_health.py), [\_\_init\_\_.py*](https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/__init__.py) and [*manifest.json*](https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/manifest.json) to `config/custom_components/notione` directory:
```bash
mkdir -p custom_components/notione
cd custom_components/notione
wget https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/device_tracker.py
wget https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/system_health.py
wget https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/manifest.json
wget https://github.com/n4ts/ha-notione/raw/master/custom_components/notione/__init__.py
```

[releases]: https://github.com/n4ts/ha-notione/releases
[releases-shield]: https://img.shields.io/github/release/n4ts/ha-notione.svg?style=for-the-badge
[downloads-total-shield]: https://img.shields.io/github/downloads/n4ts/ha-notione/total?style=for-the-badge
[hacs-badge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs-badge-url]: https://github.com/custom-components/hacs
[paypal-me-shield]: https://img.shields.io/badge/PayPal.Me-stanpielak-blue?style=for-the-badge
[paypal-me]: https://www.paypal.me/stanpielak

