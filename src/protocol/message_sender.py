# protocol/message_sender.py
import uuid
import time
from custom_logging.logger import log_message
from network.utils import send_message
from config import settings  # ✅ Use global VERBOSE_MODE

async def send_ping(peer_ip, peer_port, user_id):
    verbose = settings.VERBOSE_MODE
    message = (
        f"TYPE: PING\nUSER_ID: {user_id}\n\n"
        if verbose else f"PING|{user_id}\n"
    )
    if verbose:
        log_message(f"Sending PING: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_profile(peer_ip, peer_port, user_id, display_name, status):
    verbose = settings.VERBOSE_MODE
    message = (
        f"TYPE: PROFILE\nUSER_ID: {user_id}\nDISPLAY_NAME: {display_name}\nSTATUS: {status}\n\n"
        if verbose else f"PROFILE|{user_id}|{display_name}|{status}\n"
    )
    if verbose:
        log_message(f"Sending PROFILE: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_post(peer_ip, peer_port, user_id, content):
    verbose = settings.VERBOSE_MODE
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    message = (
        f"TYPE: POST\nUSER_ID: {user_id}\nCONTENT: {content}\nTTL: 3600\nMESSAGE_ID: {message_id}\nTOKEN: {user_id}|{timestamp}|broadcast\n\n"
        if verbose else f"POST|{user_id}|{content}|3600|{message_id}|{user_id}|{timestamp}|broadcast\n"
    )
    if verbose:
        log_message(f"Sending POST: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_dm(peer_ip, peer_port, from_user, to_user, content):
    verbose = settings.VERBOSE_MODE
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    message = (
        f"TYPE: DM\nFROM: {from_user}\nTO: {to_user}\nCONTENT: {content}\nTIMESTAMP: {timestamp}\nMESSAGE_ID: {message_id}\nTOKEN: {from_user}|{timestamp}|chat\n\n"
        if verbose else f"DM|{from_user}|{to_user}|{content}|{timestamp}|{message_id}|{from_user}|{timestamp}|chat\n"
    )
    if verbose:
        log_message(f"Sending DM: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_follow(peer_ip, peer_port, from_user, to_user):
    verbose = settings.VERBOSE_MODE
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    message = (
        f"TYPE: FOLLOW\nMESSAGE_ID: {message_id}\nFROM: {from_user}\nTO: {to_user}\nTIMESTAMP: {timestamp}\nTOKEN: {from_user}|{timestamp}|follow\n\n"
        if verbose else f"FOLLOW|{message_id}|{from_user}|{to_user}|{timestamp}|{from_user}|{timestamp}|follow\n"
    )
    if verbose:
        log_message(f"Sending FOLLOW: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_unfollow(peer_ip, peer_port, from_user, to_user):
    verbose = settings.VERBOSE_MODE
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    message = (
        f"TYPE: UNFOLLOW\nMESSAGE_ID: {message_id}\nFROM: {from_user}\nTO: {to_user}\nTIMESTAMP: {timestamp}\nTOKEN: {from_user}|{timestamp}|follow\n\n"
        if verbose else f"UNFOLLOW|{message_id}|{from_user}|{to_user}|{timestamp}|{from_user}|{timestamp}|follow\n"
    )
    if verbose:
        log_message(f"Sending UNFOLLOW: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_like(peer_ip, peer_port, from_user, to_user, post_timestamp):
    verbose = settings.VERBOSE_MODE
    timestamp = int(time.time())
    message = (
        f"TYPE: LIKE\nFROM: {from_user}\nTO: {to_user}\nPOST_TIMESTAMP: {post_timestamp}\nACTION: LIKE\nTIMESTAMP: {timestamp}\nTOKEN: {from_user}|{timestamp}|broadcast\n\n"
        if verbose else f"LIKE|{from_user}|{to_user}|{post_timestamp}|LIKE|{timestamp}|{from_user}|{timestamp}|broadcast\n"
    )
    if verbose:
        log_message(f"Sending LIKE: {message}")
    await send_message(message, peer_ip, peer_port)

async def send_ack(peer_ip, peer_port, message_id):
    verbose = settings.VERBOSE_MODE
    message = (
        f"TYPE: ACK\nMESSAGE_ID: {message_id}\nSTATUS: RECEIVED\n\n"
        if verbose else f"ACK|{message_id}|RECEIVED\n"
    )
    if verbose:
        log_message(f"Sending ACK: {message}")
    await send_message(message, peer_ip, peer_port)
