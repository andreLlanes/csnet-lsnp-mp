import asyncio
import socket

async def send_message(message: str, peer_ip: str, port: int):
    """Send a message via UDP to the peer."""
    loop = asyncio.get_event_loop()  # Get the event loop
    # Run the blocking socket.sendto() in the event loop executor to make it async
    await loop.run_in_executor(None, _send, message, peer_ip, port)

def _send(message: str, peer_ip: str, port: int):
    """Synchronous send function that is executed in the event loop."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()
