# network/udp_client.py
import asyncio
import socket
from custom_logging.logger import log_message
from config.settings import UDP_PORT

async def send_message(message: str, peer_ip: str, peer_port: int = UDP_PORT):
    """Send a message to a peer."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, peer_port))
    log_message(f"Sent message: {message}")
    sock.close()

async def start_sending():
    # Example to start sending a message to a specific peer
    peer_ip = "192.168.1.100"  # Just an example
    message = "TYPE: PING\nUSER_ID: alice@192.168.1.10\n\n"
    await send_message(message, peer_ip)
