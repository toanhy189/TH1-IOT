"""Bai 1: publish a welcome message to iot/lab/message."""

import argparse
import os
import time

from mqtt_common import MESSAGE_TOPIC, publish, start_client, stop_client, wait_ready


def main():
    parser = argparse.ArgumentParser(description="Gui loi chao qua MQTT")
    parser.add_argument("--name", default=os.getenv("STUDENT_NAME"), required=False, help="Ho ten sinh vien")
    parser.add_argument("--student-id", default=os.getenv("STUDENT_ID"), help="Ma sinh vien")
    parser.add_argument("--message", default="Xin chao tu client Python MQTT")
    parser.add_argument("--count", type=int, default=1, help="So lan gui (mac dinh: 1)")
    parser.add_argument("--interval", type=float, default=1, help="So giay giua cac lan gui")
    args = parser.parse_args()
    if not args.name or not args.student_id:
        parser.error("Can --name va --student-id (hoac STUDENT_NAME va STUDENT_ID).")
    if args.count < 1 or args.interval < 0:
        parser.error("--count phai >= 1 va --interval phai >= 0.")

    client, ready = start_client()
    try:
        for number in range(args.count):
            wait_ready(ready)
            payload = f"{args.message} - {args.student_id} - {args.name}"
            publish(client, MESSAGE_TOPIC, payload)
            print(f"Da gui [{number + 1}/{args.count}] {MESSAGE_TOPIC}: {payload}")
            if number + 1 < args.count:
                time.sleep(args.interval)
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
