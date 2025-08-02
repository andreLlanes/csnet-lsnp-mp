# network/udp_client.py
import asyncio
import socket
from custom_logging.logger import log_message  # Make sure custom_logging is imported correctly
from config.settings import UDP_PORT

async def send_message(message: str, peer_ip: str, peer_port: int = UDP_PORT):
    """Send a message to a peer."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, peer_port))
    log_message(f"Sent message: {message}")
    sock.close()

async def send_ping(peer_ip: str):
    """Send a PING message to let others know this peer is online."""
    message = "TYPE: PING\nUSER_ID: alice@192.168.1.10\n\n"
    await send_message(message, peer_ip)

async def start_sending():
    """Periodically send PING messages to other peers."""
    peer_ip = "192.168.1.255"  # Broadcast to the entire local network
    while True:
        await send_ping(peer_ip)
        await asyncio.sleep(5)  # Send every 5 seconds
