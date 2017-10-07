import requests,logging
from homeassistant.const import (CONF_PASSWORD, CONF_URL)
from homeassistant.helpers.entity import Entity


STATE_ATTR_REASON = 'reason for status'
STATE_ATTR_STATION = 'station number'
STATE_ATTR_MASTER = 'master station number'
STATE_ATTR_PROGRAM = 'program name'
STATE_ATTR_REMAINING = 'run time remaining'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    _LOGGER = logging.getLogger(__name__)

    api_pass = config.get(CONF_PASSWORD)
    api_url = config.get(CONF_URL)

    if api_pass is None :
        r = requests.get(api_url+'/api/status')
        r = r.json()
    else:
        r = requests.get(api_url+'/api/status?pw='+api_pass)
        r = r.json()

    total_valves = len(r)

    station = 0
    all_sensors = []
    for i in r:
        if station <= total_valves:
            all_sensors.extend([SIP(station,api_url,api_pass)])
            station = station + 1

    add_devices(all_sensors)

class SIP(Entity):
    """Representation of a Sensor."""

    def __init__(self,station,api_url,api_pass):
        """Initialize the sensor."""
        self._state = None
        self._station = station
        self._api_url = api_url
        self._api_pass = api_pass

    def icon(self):
        return 'mdi:water'


    @property
    def name(self):
        """Return the name of the sensor."""
        r = []
        if self._api_pass is None :
            r = requests.get(self._api_url+'/api/status')
            r = r.json()
        else:
            r = requests.get(self._api_url+'/api/status?pw='+self._api_pass)
            r = r.json()
        return "SIP "+r[self._station]["name"]

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

        return {
                STATE_ATTR_REASON: r[self._station]["reason"],
                STATE_ATTR_STATION: self._station,
                STATE_ATTR_MASTER: r[self._station]["master"],
                STATE_ATTR_PROGRAM: r[self._station]["programName"],
                STATE_ATTR_REMAINING: r[self._station]["remaining"]
                }
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        r = []
        if self._api_pass is None:
            r = requests.get(self._api_url+'/api/status')
            r = r.json()
        else:
            r = requests.get(self._api_url+'/api/status?pw='+self._api_pass)
            r = r.json()

        self._state = r[self._station]["status"]
