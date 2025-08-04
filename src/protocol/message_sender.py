import uuid
import time
from network.utils import send_message

async def send_ttt_invite(peer_ip, game_id, from_user, to_user, symbol, verbose=True):
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    token = f"{from_user}|{timestamp}|game"
    if verbose:
        message = (
            f"TYPE: TICTACTOE_INVITE\nFROM: {from_user}\nTO: {to_user}\nGAMEID: {game_id}\nMESSAGE_ID: {message_id}\nSYMBOL: {symbol}\nTIMESTAMP: {timestamp}\nTOKEN: {token}\n"
        )
    else:
        message = f"TICTACTOE_INVITE|{from_user}|{to_user}|{game_id}|{message_id}|{symbol}|{timestamp}|{token}\n"
    await send_message(message, peer_ip, 51000)

async def send_ttt_move(peer_ip, game_id, from_user, to_user, message_id, position, symbol, turn, verbose=True):
    token = f"{from_user}|{int(time.time())}|game"
    if verbose:
        message = (
            f"TYPE: TICTACTOE_MOVE\nFROM: {from_user}\nTO: {to_user}\nGAMEID: {game_id}\nMESSAGE_ID: {message_id}\nPOSITION: {position}\nSYMBOL: {symbol}\nTURN: {turn}\nTOKEN: {token}\n"
        )
    else:
        message = f"TICTACTOE_MOVE|{from_user}|{to_user}|{game_id}|{message_id}|{position}|{symbol}|{turn}|{token}\n"
    await send_message(message, peer_ip, 51000)

async def send_ttt_result(peer_ip, game_id, from_user, to_user, message_id, result, symbol, winning_line, timestamp, verbose=True):
    if verbose:
        message = (
            f"TYPE: TICTACTOE_RESULT\nFROM: {from_user}\nTO: {to_user}\nGAMEID: {game_id}\nMESSAGE_ID: {message_id}\nRESULT: {result}\nSYMBOL: {symbol}\nWINNING_LINE: {winning_line}\nTIMESTAMP: {timestamp}\n"
        )
    else:
        message = f"TICTACTOE_RESULT|{from_user}|{to_user}|{game_id}|{message_id}|{result}|{symbol}|{winning_line}|{timestamp}\n"
    await send_message(message, peer_ip, 51000)
import uuid
import time
from custom_logging.logger import log_message
from network.utils import send_message  # Import send_message from utils.py

async def send_ping(peer_ip: str, user_id: str, port: int, verbose: bool = True):
    """Send a PING message for presence signaling."""
    if verbose:
        message = f"TYPE: PING\nUSER_ID: {user_id}\n\n"
    else:
        message = f"PING|{user_id}\n"
    log_message(f"Sending PING message: {message}")
    await send_message(message, peer_ip, port)

async def send_profile(peer_ip: str, user_id: str, display_name: str, status: str, port: int, verbose: bool = True):
    """Send a PROFILE message to announce a user's identity."""
    if verbose:
        message = f"TYPE: PROFILE\nUSER_ID: {user_id}\nDISPLAY_NAME: {display_name}\nSTATUS: {status}\n\n"
    else:
        message = f"PROFILE|{user_id}|{display_name}|{status}\n"
    log_message(f"Sending PROFILE message: {message}")
    await send_message(message, peer_ip, port)

async def send_post(peer_ip: str, content: str, verbose: bool = True):
    """Send a POST message to all peers."""
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    if verbose:
        message = f"TYPE: POST\nUSER_ID: andre@192.168.1.10\nCONTENT: {content}\nTTL: 3600\nMESSAGE_ID: {message_id}\nTOKEN: andre@192.168.1.10|{timestamp}|broadcast\n\n"
    else:
        message = f"POST|andre@192.168.1.10|{content}|3600|{message_id}|andre@192.168.1.10|{timestamp}|broadcast\n"
    log_message(f"Sending POST message: {message}")
    await send_message(message, peer_ip, 51000)

async def send_dm(peer_ip: str, to_user: str, content: str, verbose: bool = True):
    """Send a Direct Message (DM) to a specific peer."""
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    if verbose:
        message = f"TYPE: DM\nFROM: andre@192.168.1.10\nTO: {to_user}\nCONTENT: {content}\nTIMESTAMP: {timestamp}\nMESSAGE_ID: {message_id}\nTOKEN: andre@192.168.1.10|{timestamp}|chat\n\n"
    else:
        message = f"DM|andre@192.168.1.10|{to_user}|{content}|{timestamp}|{message_id}|andre@192.168.1.10|{timestamp}|chat\n"
    log_message(f"Sending DM message: {message}")
    await send_message(message, peer_ip, 51000)

async def send_follow(peer_ip: str, to_user: str, verbose: bool = True):
    """Send a FOLLOW message to a specific user."""
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    if verbose:
        message = f"TYPE: FOLLOW\nMESSAGE_ID: {message_id}\nFROM: andre@192.168.1.10\nTO: {to_user}\nTIMESTAMP: {timestamp}\nTOKEN: andre@192.168.1.10|{timestamp}|follow\n\n"
    else:
        message = f"FOLLOW|{message_id}|andre@192.168.1.10|{to_user}|{timestamp}|andre@192.168.1.10|{timestamp}|follow\n"
    log_message(f"Sending FOLLOW message: {message}")
    await send_message(message, peer_ip, 51000)

async def send_unfollow(peer_ip: str, to_user: str, verbose: bool = True):
    """Send an UNFOLLOW message to a specific user."""
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())
    if verbose:
        message = f"TYPE: UNFOLLOW\nMESSAGE_ID: {message_id}\nFROM: andre@192.168.1.10\nTO: {to_user}\nTIMESTAMP: {timestamp}\nTOKEN: andre@192.168.1.10|{timestamp}|follow\n\n"
    else:
        message = f"UNFOLLOW|{message_id}|andre@192.168.1.10|{to_user}|{timestamp}|andre@192.168.1.10|{timestamp}|follow\n"
    log_message(f"Sending UNFOLLOW message: {message}")
    await send_message(message, peer_ip, 51000)

async def send_like(peer_ip: str, post_timestamp: str, verbose: bool = True):
    """Send a LIKE message for a specific post."""
    timestamp = int(time.time())
    if verbose:
        message = f"TYPE: LIKE\nFROM: andre@192.168.1.10\nTO: dave@192.168.1.10\nPOST_TIMESTAMP: {post_timestamp}\nACTION: LIKE\nTIMESTAMP: {timestamp}\nTOKEN: andre@192.168.1.10|{timestamp}|broadcast\n\n"
    else:
        message = f"LIKE|andre@192.168.1.10|dave@192.168.1.10|{post_timestamp}|LIKE|{timestamp}|andre@192.168.1.10|{timestamp}|broadcast\n"
    log_message(f"Sending LIKE message: {message}")
    await send_message(message, peer_ip, 51000)

async def send_ack(peer_ip: str, message_id: str, verbose: bool = True):
    """Send an ACK message to acknowledge receipt of a message."""
    if verbose:
        message = f"TYPE: ACK\nMESSAGE_ID: {message_id}\nSTATUS: RECEIVED\n\n"
    else:
        message = f"ACK|{message_id}|RECEIVED\n"
    await send_message(message, peer_ip, 51000)