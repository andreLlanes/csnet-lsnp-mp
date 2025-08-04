import socket
import time
from protocol.message_parser import craft_message

BIND_IP = "127.0.0.1"
PORT_ALICE = 51000
PORT_BOB = 51001

def send_msg(msg_type, kv_pairs, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = craft_message(msg_type=msg_type, kv_pairs=kv_pairs)
    sock.sendto(payload.encode("utf-8"), (BIND_IP, target_port))
    sock.close()
    print(f"[TEST] Sent to {target_port}:\n{payload.strip()}\n")

def main():
    alice_id = f"alice@{BIND_IP}"
    bob_id = f"bob@{BIND_IP}"

    print("[TEST] Starting Milestone 2 tests...")

    # 1️⃣ Test POST
    send_msg("POST", {"USER_ID": alice_id, "CONTENT": "Hello Bob!"}, PORT_BOB)
    send_msg("POST", {"USER_ID": bob_id, "CONTENT": "Hello Alice!"}, PORT_ALICE)
    time.sleep(1)

    # 2️⃣ Test DM
    send_msg("DM", {"FROM": alice_id, "TO": bob_id, "CONTENT": "Private hi Bob!"}, PORT_BOB)
    send_msg("DM", {"FROM": bob_id, "TO": alice_id, "CONTENT": "Private hi Alice!"}, PORT_ALICE)
    time.sleep(1)

    # 3️⃣ Test FOLLOW
    send_msg("FOLLOW", {"FROM": alice_id, "TO": bob_id}, PORT_BOB)
    send_msg("FOLLOW", {"FROM": bob_id, "TO": alice_id}, PORT_ALICE)
    time.sleep(1)

    # 4️⃣ Test UNFOLLOW
    send_msg("UNFOLLOW", {"FROM": alice_id, "TO": bob_id}, PORT_BOB)
    send_msg("UNFOLLOW", {"FROM": bob_id, "TO": alice_id}, PORT_ALICE)
    time.sleep(1)

    print("[TEST] Milestone 2 message simulation done.")

if __name__ == "__main__":
    main()
