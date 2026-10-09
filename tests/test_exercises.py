"""Small offline checks for payloads, alert boundaries, and light responses."""

import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace

import device_bai3
import monitor_subscriber_bai2
from mqtt_common import (
    LIGHT_STATUS_TOPIC, light_status_payload, parse_sensor,
    sensor_alerts, sensor_payload,
)


class ExerciseTests(unittest.TestCase):
    def test_sensor_json_and_alert_boundaries(self):
        data = parse_sensor(sensor_payload(35, 40))
        self.assertEqual(data, {"device_id": "sensor01", "temperature": 35.0, "humidity": 40.0})
        self.assertEqual(sensor_alerts(data), [])
        data = parse_sensor(sensor_payload(36.1, 38.7))
        self.assertEqual(sensor_alerts(data), [
            "CANH BAO: Nhiet do cao", "CANH BAO: Do am thap",
        ])

    def test_monitor_rejects_bad_sensor_payload(self):
        with self.assertRaises(ValueError):
            parse_sensor(b'{"device_id":"sensor01","temperature":true,"humidity":50}')
        output = io.StringIO()
        with redirect_stdout(output):
            monitor_subscriber_bai2.on_message(None, None, SimpleNamespace(payload=b"not json"))
        self.assertIn("Bo qua payload khong hop le", output.getvalue())

    def test_light_device_publishes_only_valid_commands(self):
        class FakeClient:
            def __init__(self):
                self.messages = []

            def publish(self, topic, payload, qos):
                self.messages.append((topic, payload, qos))
                return SimpleNamespace(rc=0)

        client = FakeClient()
        output = io.StringIO()
        with redirect_stdout(output):
            device_bai3.on_message(client, None, SimpleNamespace(payload=b"on"))
            device_bai3.on_message(client, None, SimpleNamespace(payload=b"BAD"))
            device_bai3.on_message(client, None, SimpleNamespace(payload=b"OFF"))
        self.assertEqual(client.messages, [
            (LIGHT_STATUS_TOPIC, light_status_payload("ON"), 1),
            (LIGHT_STATUS_TOPIC, light_status_payload("OFF"), 1),
        ])
        self.assertEqual(json.loads(client.messages[0][1])["status"], "ON")
        self.assertIn("Bo qua lenh khong hop le", output.getvalue())


if __name__ == "__main__":
    unittest.main()
