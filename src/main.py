import socket
import threading
import argparse
from custom_logging.logger import set_verbose, log
from parser import parse_message, handle_message

def listener(sock, peers, posts, dms):
    while True:
        raw, addr = sock.recvfrom(65535)
        raw_str = raw.decode(errors="ignore")
        log(f"RECV < {raw_str.strip()}", verbose_only=True)

        data = parse_message(raw_str)
        handle_message(data, peers, posts, dms)

def main():
    parser = argparse.ArgumentParser(description="LSNP Peer Client")
    parser.add_argument("username", help="Username for LSNP")
    parser.add_argument("ip", help="Local IP to bind")
    parser.add_argument("listen_port", type=int, help="Port to listen on")
    parser.add_argument("send_port", type=int, help="Port to send to")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    set_verbose(args.verbose)

    peers = {}
    posts = []
    dms = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.ip, args.listen_port))

    threading.Thread(target=listener, args=(sock, peers, posts, dms), daemon=True).start()

    log(f"Peer {args.username} started on {args.ip}:{args.listen_port}")

    try:
        while True:
            msg = input("> ")
            if msg.lower() == "/quit":
                break
            elif msg.startswith("/post "):
                content = msg[len("/post "):]
                payload = f"TYPE: POST\nUSER_ID: {args.username}@{args.ip}\nCONTENT: {content}\n\n"
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)
            elif msg.startswith("/profile "):
                status = msg[len("/profile "):]
                payload = f"TYPE: PROFILE\nUSER_ID: {args.username}@{args.ip}\nDISPLAY_NAME: {args.username}\nSTATUS: {status}\n\n"
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)
            elif msg.startswith("/dm "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    to_user, content = parts[1], parts[2]
                    payload = f"TYPE: DM\nFROM: {args.username}@{args.ip}\nTO: {to_user}\nCONTENT: {content}\n\n"
                    sock.sendto(payload.encode(), (args.ip, args.send_port))
                    log(f"SEND > {payload.strip()}", verbose_only=True)
            else:
                log("Unknown command. Use /post, /profile, /dm")

    except KeyboardInterrupt:
        log("Shutting down...")

if __name__ == "__main__":
    main()
