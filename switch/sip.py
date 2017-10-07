import requests,logging

import voluptuous as vol
# Need to add some config validation
from homeassistant.components.switch import (PLATFORM_SCHEMA,SwitchDevice)
from homeassistant.const import (DEVICE_DEFAULT_NAME, CONF_PASSWORD, CONF_URL)
from homeassistant.helpers.entity import ToggleEntity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

STATE_ATTR_REASON = 'reason for status'
STATE_ATTR_STATION = 'station number'
STATE_ATTR_MASTER = 'master station number'
STATE_ATTR_PROGRAM = 'program name'
STATE_ATTR_REMAINING = 'run time remaining'


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform."""

    api_pass = config.get(CONF_PASSWORD)
    api_url = config.get(CONF_URL)
    if api_pass is None :
        r = requests.get(str(api_url)+'/api/status')
        r = r.json()
    else:
        r = requests.get(str(api_url)+'/api/status?pw='+api_pass)
        r = r.json()

    total_valves = len(r)

    count = 0
    all_switches = []
    for i in r:
        if count <= total_valves:
            # We don't pass count as station since this may not match if all stations are not enabled
            int_station = int(i["station"])
            all_switches.extend([SIP(int(i["station"]),i["name"],api_url,api_pass)])
            count = count + 1

    add_devices(all_switches)

class SIP(SwitchDevice):
    def __init__(self,station_no,station_name,api_url,api_pass):
        """Initialize the sensor."""
        self._state = None
        self._station = station_no
        self._station_name = station_name
        self._api_url = api_url
        self._api_pass = api_pass

    @property
    def name(self):
        """Return the name of the switch."""

        return "SIP "+self._station_name

    @property
    def should_poll(self):
        """ polling needed."""
        return True

    @property
    def is_on(self):
        """Return true if device is on."""

        r = []
        if self._api_pass is None :
            r = requests.get(self._api_url+'/api/status')
            r = r.json()
        else:
            r = requests.get(self._api_url+'/api/status?pw='+self._api_pass)
            r = r.json()

        for i in r:
            if int(i["station"]) == self._station:
                if i["status"] == "on":
                    return True

    def turn_on(self, **kwargs):
        """Turn the device on."""
        if self._api_pass is None :
            requests.get(self._api_url+'/sn?sid='+str(self._station+1)+'&set_to=1')
        else:
            requests.get(self._api_url+'/sn?pw='+self._api_pass+'&sid='+str(self._station+1)+'&set_to=1')

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        if self._api_pass is None :
            requests.get(self._api_url+'/sn?sid='+str(self._station+1)+'&set_to=0')
        else:
            requests.get(self._api_url+'/sn?pw='+self._api_pass+'&sid='+str(self._station+1)+'&set_to=0')
        self.schedule_update_ha_state()

    @property
    def state_attributes(self):
        """Return the state attributes of the valves"""
        r = []
        if self._api_pass is None:
            r = requests.get(self._api_url+'/api/status')
            r = r.json()
        else:
            r = requests.get(self._api_url+'/api/status?pw='+self._api_pass)
            r = r.json()

        for i in r:
            if int(i["station"]) == self._station:
                return {
                        STATE_ATTR_REASON: i["reason"],
                        STATE_ATTR_STATION: i["station"],
                        STATE_ATTR_MASTER: i["master"],
                        STATE_ATTR_PROGRAM: i["programName"],
                        STATE_ATTR_REMAINING: i["remaining"]
                        }
