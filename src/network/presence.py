import threading
import time
import socket
from protocol.message_parser import craft_message
from custom_logging.logger import log

def start_presence_broadcast(sock, user_id, display_name, status, broadcast_ip, port, interval=10):
    """
    Broadcasts PING and PROFILE messages every `interval` seconds.
    """
    def broadcast_loop():
        while True:
            try:
                # Send PING
                ping_msg = craft_message(
                    msg_type="PING",
                    kv_pairs={
                        "USER_ID": user_id
                    }
                )
                sock.sendto(ping_msg.encode("utf-8"), (broadcast_ip, port))
                log(f"SEND > {ping_msg.strip()}", verbose_only=True)

                # Send PROFILE
                profile_msg = craft_message(
                    msg_type="PROFILE",
                    kv_pairs={
                        "USER_ID": user_id,
                        "DISPLAY_NAME": display_name,
                        "STATUS": status
                    }
                )
                sock.sendto(profile_msg.encode("utf-8"), (broadcast_ip, port))
                log(f"SEND > {profile_msg.strip()}", verbose_only=True)

                time.sleep(interval)
            except Exception as e:
                log(f"[ERROR] Presence broadcast failed: {e}")

    thread = threading.Thread(target=broadcast_loop, daemon=True)
    thread.start()
