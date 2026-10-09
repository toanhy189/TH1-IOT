"""Shared broker configuration and MQTT helpers for the three lab exercises."""

import json
import os
import sys
from threading import Event

import paho.mqtt.client as mqtt


MESSAGE_TOPIC = "iot/lab/message"
SENSOR_TOPIC = "iot/lab/sensor01/data"
LIGHT_COMMAND_TOPIC = "iot/lab/light01/cmd"
LIGHT_STATUS_TOPIC = "iot/lab/light01/status"


def start_client(subscriptions=(), on_message=None):
    """Connect and start the network loop; ready is set after subscriptions."""
    ready = Event()
    pending = set()
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    username = os.getenv("MQTT_USERNAME")
    if username:
        client.username_pw_set(username, os.getenv("MQTT_PASSWORD"))

    use_tls = os.getenv("MQTT_TLS", "0").lower() in ("1", "true", "yes")
    if use_tls:
        client.tls_set()

    def on_connect(client, _userdata, _flags, reason_code, _properties):
        ready.clear()
        pending.clear()
        if reason_code.is_failure:
            print(f"Ket noi MQTT that bai: {reason_code}", file=sys.stderr)
            return
        if not subscriptions:
            ready.set()
            return
        for topic in subscriptions:
            result, mid = client.subscribe(topic, qos=1)
            if result != mqtt.MQTT_ERR_SUCCESS:
                print(f"Khong subscribe duoc {topic}: {mqtt.error_string(result)}", file=sys.stderr)
                return
            pending.add(mid)

    def on_subscribe(_client, _userdata, mid, reason_codes, _properties):
        if any(code.is_failure for code in reason_codes):
            print("Broker tu choi subscribe.", file=sys.stderr)
            return
        pending.discard(mid)
        if not pending:
            ready.set()

    def on_disconnect(_client, _userdata, _flags, _reason_code, _properties):
        ready.clear()

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    host = os.getenv("MQTT_HOST", "localhost")
    try:
        port = int(os.getenv("MQTT_PORT", "8883" if use_tls else "1883"))
    except ValueError as exc:
        raise ValueError("MQTT_PORT phai la so nguyen.") from exc
    try:
        client.connect(host, port, keepalive=60)
    except OSError as exc:
        raise ConnectionError(f"Khong the ket noi broker {host}:{port}: {exc}") from exc
    client.loop_start()
    return client, ready


def wait_ready(ready, timeout=10):
    if not ready.wait(timeout):
        raise TimeoutError("Khong the ket noi/subscribe MQTT trong 10 giay. Kiem tra broker va thong tin dang nhap.")


def publish(client, topic, payload):
    info = client.publish(topic, payload, qos=1)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"Khong gui duoc MQTT: {mqtt.error_string(info.rc)}")
    info.wait_for_publish(timeout=10)
    if not info.is_published():
        raise TimeoutError("Broker khong xac nhan thong diep trong 10 giay.")


def stop_client(client):
    client.disconnect()
    client.loop_stop()


def sensor_payload(temperature, humidity):
    return json.dumps({
        "device_id": "sensor01",
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
    })


def parse_sensor(payload):
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Payload phai la JSON object.")
    if not isinstance(data.get("device_id"), str):
        raise ValueError("device_id phai la chuoi.")
    for field in ("temperature", "humidity"):
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} phai la so.")
    return data


def sensor_alerts(data):
    alerts = []
    if data["temperature"] > 35:
        alerts.append("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        alerts.append("CANH BAO: Do am thap")
    return alerts


def light_status_payload(status):
    return json.dumps({"device_id": "light01", "status": status})
