"""Bai 3: light device receives ON/OFF and publishes its new state."""

import time

import paho.mqtt.client as mqtt

from mqtt_common import (
    LIGHT_COMMAND_TOPIC, LIGHT_STATUS_TOPIC, light_status_payload,
    start_client, stop_client, wait_ready,
)


def on_message(client, _userdata, message):
    command = message.payload.decode("utf-8", errors="replace").strip().upper()
    if command not in ("ON", "OFF"):
        print(f"Bo qua lenh khong hop le: {command!r}", flush=True)
        return
    payload = light_status_payload(command)
    info = client.publish(LIGHT_STATUS_TOPIC, payload, qos=1)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Khong gui duoc trang thai: {mqtt.error_string(info.rc)}", flush=True)
        return
    print(f"Den light01: {command}; da gui {LIGHT_STATUS_TOPIC}: {payload}", flush=True)


def main():
    client, ready = start_client((LIGHT_COMMAND_TOPIC,), on_message)
    try:
        wait_ready(ready)
        print(f"Den light01 dang nghe {LIGHT_COMMAND_TOPIC}. Nhan Ctrl+C de dung.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung thiet bi.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
