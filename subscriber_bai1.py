"""Bai 1: receive welcome messages and print their arrival time."""

from datetime import datetime
import time

from mqtt_common import MESSAGE_TOPIC, start_client, stop_client, wait_ready


def on_message(_client, _userdata, message):
    print("Nhan duoc message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload.decode('utf-8', errors='replace')}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n", flush=True)


def main():
    client, ready = start_client((MESSAGE_TOPIC,), on_message)
    try:
        wait_ready(ready)
        print(f"Dang lang nghe {MESSAGE_TOPIC}. Nhan Ctrl+C de dung.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung subscriber.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
