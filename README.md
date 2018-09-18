# kodi-db
A Kodi watched item to database script

This is a personal mini trakt.tv like script without all the bling

Example usage from Home Assistant automation
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
  store_in_kodi: '/home/homeassistant/kodi-db.py -s MONGO_SERVER-c {{ states.media_player.kodi.attributes.media_content_type}} -t "{{ states.media_player.kodi.attributes.media_title }}"'

```
