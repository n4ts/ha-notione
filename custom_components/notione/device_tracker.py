"""Support for notiOne® Bluetooth trackers."""

from datetime import datetime,timedelta
import logging

import requests,json

import voluptuous as vol

from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_utc_time_change
from homeassistant.util import slugify
from homeassistant.util import dt

import urllib3
urllib3.disable_warnings()

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=300)
MDI_ICON = 'mdi:bluetooth-connect'

token_url = 'https://auth.notinote.me/oauth/token'
list_url = 'https://api.notinote.me/secured/internal/devicelist'

auth_login = 'test-oauth-client-id'
auth_pass = '$2y$12$vXOUtEenVFCO1Zgy2YiePuF3WF/sDgNO3YnhRjl49NIDlEbGeSeOu'

grant_type = 'password'
scope = 'NOTI'

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

        data = {
          'grant_type': grant_type,
          'username': self.username,
          'password': self.password,
          'scope': scope
        }

        access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(auth_login, auth_pass))

        tokens = json.loads(access_token_response.text)
        access_token = tokens['access_token']

        api_call_headers = {'Authorization': 'Bearer ' + access_token}
        api_call_response = requests.get(list_url, headers=api_call_headers, verify=False)

        json_object = json.loads(api_call_response.text)

        for dev in json_object['deviceList']:

            tracker_id = dev['deviceId']
            dev_id = dev['name']

            _LOGGER.info('New device: %s', dev_id)

            if dev_id is None:
                dev_id = tracker_id

            lat = dev['lastPosition']['latitude']
            lon = dev['lastPosition']['longitude']
            beaconid = dev['deviceId']
            deviceVersion = dev['deviceVersion']
            gpstime = datetime.fromtimestamp(dev['lastPosition']['gpstime']/1000.0)
            entity_picture = dev['avatar']
            accuracy = dev['lastPosition']['accuracy']
            city = dev['lastPosition']['geocodeCity']
            street = dev['lastPosition']['geocodePlace']
            battery = dev['notiOneDetails']['battery']
            mac = dev['notiOneDetails']['mac']

            if city is None:
                city = ''
            if street is None:
                street = ''

            if battery:
                battery_status = 'low'
            else:
                battery_status = 'high'

            if entity_picture[0:4] != 'http':
                entity_picture = ''

            attrs = {
                'friendly_name': dev_id ,
                'gpstime': gpstime ,
                'entity_picture': entity_picture ,
                'beaconid': beaconid ,
                'location': street + ',' + city ,
                'battery_status': battery_status ,
                'deviceVersion': deviceVersion , 
                'icon': MDI_ICON
            }

            self.see(
                dev_id=tracker_id, host_name=dev_id, mac=mac, gps=(lat, lon), gps_accuracy=accuracy, attributes=attrs
            )
