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

            # Step 1: HELLO handshake
            if parsed.get("TYPE") == "HELLO":
                self.send_message(addr, "ACK", {
                    "message": "Handshake successful"
                })
            # Step 2: Echo back messages
            elif parsed.get("TYPE") == "MESSAGE":
                self.send_message(addr, "REPLY", {
                    "content": f"Server got: {parsed.get('content', '')}"
                })
            else:
                self.send_message(addr, "ERROR", {
                    "error": "Unknown message type"
                })


if __name__ == "__main__":
    server = UDPServer("0.0.0.0", 5000, verbose=True)
    server.run()
