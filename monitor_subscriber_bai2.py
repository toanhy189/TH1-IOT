"""Bai 2: display sensor data and warn when thresholds are crossed."""

import json
import time

from mqtt_common import SENSOR_TOPIC, parse_sensor, sensor_alerts, start_client, stop_client, wait_ready


def on_message(_client, _userdata, message):
    try:
        data = parse_sensor(message.payload)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Bo qua payload khong hop le: {exc}", flush=True)
        return
    print(f"Device: {data['device_id']}")
    print(f"Temperature: {data['temperature']:.1f} C")
    print(f"Humidity: {data['humidity']:.1f} %")
    for alert in sensor_alerts(data):
        print(alert)
    print(flush=True)


def main():
    client, ready = start_client((SENSOR_TOPIC,), on_message)
    try:
        wait_ready(ready)
        print(f"Dang lang nghe {SENSOR_TOPIC}. Nhan Ctrl+C de dung.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung monitor.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
