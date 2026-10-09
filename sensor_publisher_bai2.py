"""Bai 2: simulate temperature and humidity every three seconds."""

import argparse
import random
import time

from mqtt_common import SENSOR_TOPIC, publish, sensor_payload, start_client, stop_client, wait_ready


def main():
    parser = argparse.ArgumentParser(description="Mo phong cam bien sensor01")
    parser.add_argument("--count", type=int, help="So mau can gui; bo qua de gui lien tuc")
    parser.add_argument("--interval", type=float, default=3, help="Chu ky gui, giay (mac dinh: 3)")
    args = parser.parse_args()
    if (args.count is not None and args.count < 1) or args.interval < 0:
        parser.error("--count phai >= 1 va --interval phai >= 0.")

    client, ready = start_client()
    sent = 0
    try:
        while args.count is None or sent < args.count:
            wait_ready(ready)
            payload = sensor_payload(random.uniform(20, 40), random.uniform(30, 80))
            publish(client, SENSOR_TOPIC, payload)
            sent += 1
            print(f"Da gui {SENSOR_TOPIC}: {payload}", flush=True)
            if args.count is None or sent < args.count:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDa dung cam bien.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
