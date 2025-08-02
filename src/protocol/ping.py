# protocol/ping.py
import asyncio
from network.udp_client import send_message
from config.settings import UDP_PORT

async def send_ping(peer_ip: str):
    """Send a PING message to let others know this peer is online."""
    message = "TYPE: PING\nUSER_ID: alice@192.168.1.10\n\n"
    await send_message(message, peer_ip)
