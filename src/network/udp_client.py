# udp_client.py
import socket
import sys
from protocol.message_parser import craft_message, parse_message


class UDPClient:
    def __init__(self, username_at_ip, target_ip, target_port, source_port, verbose=False):
        try:
            self.username, self.source_ip = username_at_ip.split("@")
        except ValueError:
            print("Error: username@ip format required.")
            sys.exit(1)

        self.target_ip = target_ip
        self.target_port = int(target_port)
        self.source_port = int(source_port)
        self.verbose = verbose

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.source_ip, self.source_port))

        if self.verbose:
            print(f"[CLIENT] {self.username} bound to {self.source_ip}:{self.source_port}")
            print(f"[CLIENT] Target: {self.target_ip}:{self.target_port}")

    def send_message(self, msg_type, kv_pairs):
        message = craft_message(msg_type, kv_pairs)
        self.sock.sendto(message.encode(), (self.target_ip, self.target_port))

        if self.verbose:
            print(f"[CLIENT] Sent:\n{message.strip()}")

    def receive_message(self):
        data, addr = self.sock.recvfrom(4096)
        decoded = data.decode()
        parsed = parse_message(decoded)

        if self.verbose:
            print(f"[CLIENT] Received raw from {addr}:\n{decoded.strip()}")
            print(f"[CLIENT] Parsed: {parsed}")

        return parsed

    def run(self):
        # Step 1: HELLO handshake
        self.send_message("HELLO", {
            "username": self.username,
            "ip": self.source_ip,
            "port": str(self.source_port)
        })

        ack = self.receive_message()
        if ack and ack.get("TYPE") == "ACK":
            print(f"[CLIENT] Server ACK: {ack}")
        else:
            print("[CLIENT] No valid ACK received. Exiting.")
            return

        # Step 2: Interactive mode
        while True:
            user_input = input("[CLIENT] Enter message (or 'quit'): ").strip()
            if user_input.lower() == "quit":
                break

            self.send_message("MESSAGE", {
                "from": self.username,
                "content": user_input
            })

            reply = self.receive_message()
            if reply:
                print(f"[CLIENT] Server reply: {reply}")


if __name__ == "__main__":
    # Example usage: python udp_client.py alice@127.0.0.1 127.0.0.1 5000 5001
    if len(sys.argv) < 5:
        print("Usage: python udp_client.py <username@ip> <target_ip> <target_port> <source_port> [--verbose]")
        sys.exit(1)

    verbose_flag = "--verbose" in sys.argv
    if verbose_flag:
        sys.argv.remove("--verbose")

    client = UDPClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], verbose=verbose_flag)
    client.run()
