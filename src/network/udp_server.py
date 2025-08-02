import asyncio
import socket
from custom_logging.logger import log_message
from network.udp_client import send_message
from protocol.profile import parse_profile, send_profile
from config.settings import RECEIVE_PORT

async def receive_message():
    """Listen for incoming messages on the UDP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', RECEIVE_PORT))  # Listen on the RECEIVE_PORT

    log_message(f"Listening for incoming messages on port {RECEIVE_PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024)  # Receiving the message
        if not data:
            log_message("No data received.")
            continue  # Skip if no data is received
        
        message = data.decode()  # Decode the message to a string
        log_message(f"Received message from {addr}: {message}")

        # Check if the message contains the PING type
        if "PING" in message:
            log_message("PING message received. Responding with PROFILE.")
            send_profile(addr[0], "gwen@192.168.1.3", "Andre", "Online", RECEIVE_PORT)  # Respond with PROFILE
        elif "PROFILE" in message:
            log_message("PROFILE message received. Parsing profile.")
            parse_profile(message)
        else:
            log_message("Received an unrecognized message.")

