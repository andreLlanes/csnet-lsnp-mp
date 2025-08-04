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
    elif message_type == "ttt_invite":
        from protocol.message_sender import send_ttt_invite
        await send_ttt_invite(peer_ip, kwargs["game_id"], kwargs["from_user"], kwargs["to_user"], kwargs["symbol"], verbose=VERBOSE_MODE)
    elif message_type == "ttt_move":
        from protocol.message_sender import send_ttt_move
        await send_ttt_move(peer_ip, kwargs["game_id"], kwargs["from_user"], kwargs["to_user"], kwargs["message_id"], kwargs["position"], kwargs["symbol"], kwargs["turn"], verbose=VERBOSE_MODE)
    elif message_type == "ttt_result":
        from protocol.message_sender import send_ttt_result
        await send_ttt_result(peer_ip, kwargs["game_id"], kwargs["from_user"], kwargs["to_user"], kwargs["message_id"], kwargs["result"], kwargs["symbol"], kwargs["winning_line"], kwargs["timestamp"], verbose=VERBOSE_MODE)
    else:
        print(f"Unknown message type: {message_type}")
        return
