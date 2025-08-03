import asyncio
from custom_logging.logger import log_message
from network.utils import send_message  # Import send_message from utils.py
from protocol.message_sender import send_post, send_dm, send_follow, send_unfollow, send_like, send_profile, send_ack, send_ping

USER_ID = "andre@192.168.1.10"  # Set your user ID here
SEND_PORT = 51000  # Default port for sending

async def send_ping_periodically(peer_ip: str, user_id: str, port: int):
    """Send PING messages every 5 seconds for presence signaling."""
    while True:
        await send_ping(peer_ip, user_id, port)
        await asyncio.sleep(5)


async def start_sending(message_type: str, peer_ip: str, **kwargs):
    """Send a message of the given type, and always start the ping loop."""
    # Start ping loop in the background
    ping_task = asyncio.create_task(send_ping_periodically(peer_ip, USER_ID, SEND_PORT))

    # Send the requested message type
    from config.settings import VERBOSE_MODE
    if message_type == "post":
        await send_post(peer_ip, kwargs.get("content", "Whatsup!"), verbose=VERBOSE_MODE)
    elif message_type == "dm":
        await send_dm(peer_ip, kwargs.get("to_user", "andre@192.168.1.12"), kwargs.get("content", "Hello gwen!"), verbose=VERBOSE_MODE)
    elif message_type == "follow":
        await send_follow(peer_ip, kwargs.get("to_user", "andre@192.168.1.10"), verbose=VERBOSE_MODE)
    elif message_type == "unfollow":
        await send_unfollow(peer_ip, kwargs.get("to_user", "andre@192.168.1.10"), verbose=VERBOSE_MODE)
    elif message_type == "profile":
        await send_profile(peer_ip, USER_ID, kwargs.get("display_name", "andre"), kwargs.get("status", "Online"), SEND_PORT, verbose=VERBOSE_MODE)
    elif message_type == "ack":
        await send_ack(peer_ip, kwargs.get("message_id", "f83d2b1c"), verbose=VERBOSE_MODE)
    else:
        print(f"Unknown message type: {message_type}")
        return

    # Keep the ping loop alive
    await ping_task
