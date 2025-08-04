import socket
import time

def send_message(sock, target_ip, target_port, message):
    sock.sendto(message.encode(), (target_ip, target_port))

def main():
    target_ip = "127.0.0.1"
    target_port = 5000  # Alice's listening port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 1️⃣ Send PING
    send_message(sock, target_ip, target_port, "TYPE: PING\nUSER_ID: bob@127.0.0.1")
    time.sleep(0.5)

    # 2️⃣ Send PROFILE
    send_message(sock, target_ip, target_port,
                 "TYPE: PROFILE\nUSER_ID: bob@127.0.0.1\nDISPLAY_NAME: Bob\nSTATUS: Hi Alice, I'm Bob.")
    time.sleep(0.5)

    # 3️⃣ Send POST
    send_message(sock, target_ip, target_port,
                 "TYPE: POST\nUSER_ID: bob@127.0.0.1\nCONTENT: Bob here, hello Alice!")
    time.sleep(0.5)

    # 4️⃣ Send DM
    send_message(sock, target_ip, target_port,
                 "TYPE: DM\nFROM: bob@127.0.0.1\nTO: alice@127.0.0.1\nCONTENT: Private message to Alice")
    time.sleep(0.5)

    # 5️⃣ Send FOLLOW
    send_message(sock, target_ip, target_port,
                 "TYPE: FOLLOW\nFROM: bob@127.0.0.1\nTO: alice@127.0.0.1")
    time.sleep(0.5)

    # 6️⃣ Send UNFOLLOW
    send_message(sock, target_ip, target_port,
                 "TYPE: UNFOLLOW\nFROM: bob@127.0.0.1\nTO: alice@127.0.0.1")
    time.sleep(0.5)

    # 7️⃣ Milestone 2 completion signal
    send_message(sock, target_ip, target_port, "TYPE: TEST_DONE")
    time.sleep(0.5)

    print("[Testing complete, waiting for responses...]")

if __name__ == "__main__":
    main()
