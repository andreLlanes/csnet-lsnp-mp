import asyncio
import socket
from custom_logging.logger import log_message
from config.settings import SEND_PORT  # Now using the SEND_PORT from settings

async def send_message(message: str, peer_ip: str, peer_port: int = SEND_PORT):
    """Send a message to a peer."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, peer_port))
    log_message(f"Sent message: {message}")
    sock.close()

async def send_ping(peer_ip: str):
    """Send a PING message to let others know this peer is online."""
    message = "TYPE: PING\nUSER_ID: alice@192.168.1.10\n\n"  # Correct message format with newlines
    log_message(f"Sending message: {message}")  # Log the message before sending
    await send_message(message, peer_ip, 51000)  # Send to port 51000, which is the receiver's port


async def start_sending():
    """Periodically send PING messages to other peers."""
    peer_ip = "192.168.1.255"  # Use loopback address for local testing
    while True:
        await send_ping(peer_ip)
        log_message("PING sent to loopback address.")
        await asyncio.sleep(5)  # Send every 5 seconds
