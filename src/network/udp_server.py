# udp_server.py
import socket
from protocol.message_parser import craft_message, parse_message


class UDPServer:
    def __init__(self, bind_ip, bind_port, verbose=False):
        self.bind_ip = bind_ip
        self.bind_port = int(bind_port)
        self.verbose = verbose

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.bind_ip, self.bind_port))

        if self.verbose:
            print(f"[SERVER] Listening on {self.bind_ip}:{self.bind_port}")

    def send_message(self, addr, msg_type, kv_pairs):
        message = craft_message(msg_type, kv_pairs)
        self.sock.sendto(message.encode(), addr)

        if self.verbose:
            print(f"[SERVER] Sent to {addr}:\n{message.strip()}")

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(4096)
            decoded = data.decode()
            parsed = parse_message(decoded)

            if self.verbose:
                print(f"[SERVER] Received raw from {addr}:\n{decoded.strip()}")
                print(f"[SERVER] Parsed: {parsed}")

            if not parsed or "TYPE" not in parsed:
                continue

            msg_type = parsed["TYPE"]

            if msg_type == "HELLO":
                username = parsed.get("USERNAME", "Unknown")
                ip = parsed.get("IP", addr[0])
                port = parsed.get("PORT", str(addr[1]))

                self.send_message(addr, "ACK", {
                    "server": "LSNP-Test",
                    "status": "Connected",
                    "your_username": username
                })

            elif msg_type == "MESSAGE":
                content = parsed.get("CONTENT", "")
                from_user = parsed.get("FROM", "Unknown")

                if self.verbose:
                    print(f"[SERVER] MESSAGE from {from_user}: {content}")

                # Echo back with LSNP format
                self.send_message(addr, "RESPONSE", {
                    "from": "server",
                    "content": f"Echo: {content}"
                })
