"""Bai 3: issue light commands and display status responses."""

from mqtt_common import (
    LIGHT_COMMAND_TOPIC, LIGHT_STATUS_TOPIC, publish,
    start_client, stop_client, wait_ready,
)


def on_message(_client, _userdata, message):
    print(f"\nTrang thai nhan duoc:\n{message.payload.decode('utf-8', errors='replace')}", flush=True)


def main():
    client, ready = start_client((LIGHT_STATUS_TOPIC,), on_message)
    try:
        wait_ready(ready)
        print("Nhap ON, OFF hoac EXIT de ket thuc.")
        while True:
            command = input("Nhap lenh: ").strip().upper()
            if command == "EXIT":
                break
            if command not in ("ON", "OFF"):
                print("Lenh khong hop le. Chi nhap ON, OFF hoac EXIT.")
                continue
            wait_ready(ready)
            publish(client, LIGHT_COMMAND_TOPIC, command)
            print(f"Da gui lenh {command} toi light01", flush=True)
    except (KeyboardInterrupt, EOFError):
        print("\nDa dung controller.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
