# kodi-db
A Kodi watched item to database script

This script connects to Kodi via WS and queries for current
video player. If anything is playing it will try to store
that name in a dB
This is a personal mini trakt.tv like script without all the bling

Example usage from Home Assistant
sensor:
  - platform: command_line
    name: Kodi-dB
    command: "/tmp/kodi-db.py -k kodi.ip:9090 -s sql.ip"
    scan_interval: 300
    value_template: '{{ value_json.name }}'

