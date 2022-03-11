Схема сообщений:
https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html#zigbee2mqtt-bridge-groups

## Исходящие события:
- Обновление стейта: topic 'zigbee2mqtt/Спальня светильник (нижняя)', payload '{"brightness":254,"color_mode":"color_temp","color_temp":250,"linkquality":70,"state":"ON","update":{"state":"available"},"update_available":true}'
- Удаление устройства: topic 'zigbee2mqtt/bridge/response/device/remove', payload '{"data":{"block":false,"force":true,"id":"Спальня светильник (пульт)"},"status":"ok","transaction":"1q3vi-2"}'

## Входящие события:
- Устройство подключено: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x50325ffffe71f9a6","ieee_address":"0x50325ffffe71f9a6"},"type":"device_joined"}'
- Устройство опрашивается: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x50325ffffe71f9a6","ieee_address":"0x50325ffffe71f9a6","status":"started"},"type":"device_interview"}'
- Устройство снова появилось в сети (напр. включили с выключателя): topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x50325ffffe71f9a6","ieee_address":"0x50325ffffe71f9a6","status":"started"},"type":"device_announce"}'
- Создается очередь с адресом устройства и устанавливаются параметры: Info MQTT publish: topic 'zigbee2mqtt/0x50325ffffe71f9a6', payload '{"action":"brightness_up_click","linkquality":76}'