## Synopsis

HomeAssistant switch and sensor integration for the SIP Python port of Opensprinkler by Dan-in-CA (https://github.com/Dan-in-CA/SIP).

This will NOT work for the original Arduino version of Opensprinkler as the APIs are completely different.

Switches will turn corresponding zones in SIP on and off. Sensors will show current state of SIP zone. Both switches and sensors include additional attributes for program name, reason for zone status, remaining run time, and station number.

SWITCHES ONLY WORK IF MANUAL MODE IS ENABLED IN SIP

A future platform that contains switches and sensors for automatic/manual mode, rain delay, run program, etc.

SIP versions prior to May 2017 will not work as the API was modified to include station names.

## Code Example

In your configuration.yaml:

    switch:
      - platform: sip
        url: http://sip.example.com
        password: !secret sip_password

    switch:
      - platform: sip
        url: http://sip.example.com
        password: !secret sip_password

## Installation

move sip.py for switch and sensor components to hass home directory /custom_components/switch and /sensor accordingly.
