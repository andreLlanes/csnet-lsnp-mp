# network/udp_server.py
import asyncio
import socket
from custom_logging.logger import log_message
from protocol.profile import parse_profile 
from config.settings import UDP_PORT
from network.udp_client import send_message

async def receive_message():
    """Listen for incoming messages on the UDP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', UDP_PORT))
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        log_message(f"Received message from {addr}: {message}")
        
        if "PING" in message:
            # Respond with PROFILE when receiving a PING message
            await send_profile(addr[0])  # Send to the same address that sent the PING
        elif "PROFILE" in message:
            # Parse the PROFILE message (you could store this info)
            profile = parse_profile(message)
            log_message(f"Received PROFILE: {profile}")

async def send_profile(peer_ip: str):
    """Send a PROFILE message in response to a PING message."""
    message = """
    TYPE: PROFILE
    USER_ID: alice@192.168.1.10
    DISPLAY_NAME: Alice
    STATUS: Online
    """
    await send_message(message, peer_ip)


async def start_receiving():
    await receive_message()
