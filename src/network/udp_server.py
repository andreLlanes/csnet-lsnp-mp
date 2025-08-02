import asyncio
import socket
from custom_logging.logger import log_message
from network.udp_client import send_message
from protocol.profile import parse_profile, send_profile  # Import send_profile function
from config.settings import RECEIVE_PORT  # Use the RECEIVE_PORT defined

async def receive_message():
    """Listen for incoming messages on the UDP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', RECEIVE_PORT))  # Listen on the RECEIVE_PORT

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        log_message(f"Received message from {addr}: {message}")

        # Handle different message types
        if "PING" in message:
            # Respond with PROFILE when receiving a PING message
            send_profile(addr[0], "alice@192.168.1.10", "Alice", "Online", RECEIVE_PORT)  # Call without await
        elif "PROFILE" in message:
            # Parse the PROFILE message (you could store this)
            parse_profile(message)
