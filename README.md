# kodi-db
A Kodi watched item to database script

This script connects to Kodi via WS and queries for current
video player. If anything is playing it will try to store
that name in a dB
This is a personal mini trakt.tv like script without all the bling

Example usage from Home Assistant
```
sensor:
  - platform: command_line
    name: Kodi-dB
    command: "/tmp/kodi-db.py -k kodi.ip:9090 -s sql.ip"
    scan_interval: 300
    value_template: '{{ value_json.name }}'
```
    
or via automation

```
- id: '123456789'
  initial_state: 'on'
  alias: Kodi playing
  trigger:
  - entity_id: media_player.kodi
    platform: state
    to: playing
  action:
    service: shell_command.store_in_kodi
    
shell_command:
  store_in_kodi: '/home/homeassistant/kodi-db.py -k kodi.inet:9090 -s sql.inet'
```
