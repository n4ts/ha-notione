"""Support for notiOne® Bluetooth trackers."""

from datetime import datetime,timedelta
import logging

import requests
import json

import voluptuous as vol

from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_utc_time_change
from homeassistant.util import slugify
from homeassistant.util import dt

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=300)
MDI_ICON = 'mdi:bluetooth-connect'

list = 'https://web.notione.com/beacon/list'
login = 'https://web.notione.com/login'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL):
        vol.All(cv.time_period, cv.positive_timedelta)
})


def setup_scanner(hass, config: dict, see, discovery_info=None):
    NotiOneTracker(hass, config, see)
    return True


class NotiOneTracker:

    def __init__(self, hass, config: dict, see) -> None:

        self.hass = hass
        self.username = config.get(CONF_USERNAME)
        self.password = config.get(CONF_PASSWORD)
        interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

        _LOGGER.info('Scan interval: %s', interval)

        self.see = see

        def update_interval(now):

            try:
                self._update_info()
            finally:
                hass.helpers.event.track_point_in_utc_time(
                    update_interval, dt.utcnow() + interval)

        update_interval(None)

    def _update_info(self, now=None) -> None:
        """Update info from notiOne."""

        _LOGGER.info("Updating device info")

        payload = {
          'username': self.username,
          'password': self.password,
        }

        ses = requests.Session()
        req = ses.post(login, data=payload, verify=False)
        res = ses.get(list, verify=False)

        json_object = json.loads(res.text)

        for dev in json_object:

            tracker_id = dev['beaconPositions']['beaconId']
            dev_id = dev['description']

            _LOGGER.info('New device: %s', dev_id)

            if dev_id is None:
                dev_id = tracker_id

            lat = dev['beaconPositions']['latitude']
            lon = dev['beaconPositions']['longitude']
            beaconid = dev['beaconPositions']['beaconId']
            gpstime = datetime.fromtimestamp(dev['beaconPositions']['gpstime']/1000.0)
            entity_picture = dev['avatarUrl']
            accuracy = dev['beaconPositions']['accuracy']
            city = dev['beaconPositions']['city']
            street = dev['beaconPositions']['street']
            battery = dev['battery']

            if city is None:
                city = ''
            if street is None:
                street = ''

            if battery:
                battery_status = 'low'
            else:
                battery_status = 'high'

            attrs = {
                'friendly_name': dev_id ,
                'gpstime': gpstime ,
                'entity_picture': entity_picture ,
                'gps_accuracy': accuracy ,
                'beaconid': beaconid ,
                'location': street + ',' +city ,
                'battery_status': battery_status ,
                'icon': MDI_ICON
            }

            self.see(
                dev_id=dev_id, gps=(lat, lon), attributes=attrs
            )