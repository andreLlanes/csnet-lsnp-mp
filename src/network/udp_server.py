import asyncio
import socket
from custom_logging.logger import log_message
from protocol.message_parser import parse_message  # Import parse_message for parsing messages
from protocol.message_sender import send_profile, send_ack  # Import send_profile to respond with PROFILE
from config.settings import RECEIVE_PORT
from config.settings import VERBOSE_MODE

async def receive_message():
    """Listen for incoming messages on the UDP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', RECEIVE_PORT))  # Listen on the RECEIVE_PORT

    


    log_message(f"Listening for incoming messages on port {RECEIVE_PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            log_message("No data received.")
            continue
        
        message = data.decode()

        if "TYPE: ACK" in message:
            # Skip processing ACK messages as they are just acknowledgments
            log_message(f"Received ACK message: {message}")
            continue  # Skip parsing this message

        # Parse the message into key-value pairs using the parse_message function
        parsed_message = parse_message(message)
        
        log_message(f"Parsed message: {parsed_message}")  # Log parsed message for debugging

        # Handle different message types based on parsed data
        if "USER_ID" in parsed_message and "PING" in message:
            if VERBOSE_MODE:
                log_message(f"PING message received: {message}")
            else:
                log_message("")  # Do not display anything in non-verbose mode
            # Respond with PROFILE (awaiting the async function)
            await send_profile(addr[0], "gwen@192.168.1.3", "Gwen", "Online", RECEIVE_PORT)

        # Handle POST message
        elif "USER_ID" in parsed_message and "CONTENT" in parsed_message and "POST" in message:
            if VERBOSE_MODE:
                log_message(f"POST message received: {message}")
            else:
                # Non-verbose: Show DISPLAY_NAME and CONTENT
                log_message(f"{addr[0]} sent: {parsed_message['CONTENT']}")

        # Handle DM message
        elif "FROM" in parsed_message and "TO" in parsed_message and "DM" in message:
            if VERBOSE_MODE:
                log_message(f"DM message received: {message}")
            else:
                # Non-verbose: Show FROM and CONTENT
                log_message(f"{parsed_message['FROM']} sent: {parsed_message['CONTENT']}")
            await send_ack(addr[0], parsed_message['MESSAGE_ID'])
                           
        # Handle LIKE message
        elif "FROM" in parsed_message and "TO" in parsed_message and "LIKE" in message:
            if VERBOSE_MODE:
                log_message(f"LIKE message received: {message}")
            else:
                # Non-verbose: Show display_name likes the post
                log_message(f"{parsed_message['FROM']} likes your post.")

        # Handle FOLLOW/UNFOLLOW message
        elif "FROM" in parsed_message and "TO" in parsed_message and "TOKEN" in parsed_message:
            # Check for UNFOLLOW first, then FOLLOW
            if "UNFOLLOW" in message or ("unfollow" in parsed_message["TOKEN"]):
                if VERBOSE_MODE:
                    log_message(f"UNFOLLOW message received: {message}")
                else:
                    log_message(f"User {parsed_message['FROM']} has unfollowed you.")
            elif "FOLLOW" in message or ("follow" in parsed_message["TOKEN"]):
                if VERBOSE_MODE:
                    log_message(f"FOLLOW message received: {message}")
                else:
                    log_message(f"User {parsed_message['FROM']} has followed you.")
        
        # Handle PROFILE message
        elif "USER_ID" in parsed_message and "DISPLAY_NAME" in parsed_message and "STATUS" in parsed_message and "PROFILE" in message:
            if VERBOSE_MODE:
                log_message(f"PROFILE message received: {message}")
            else:
                log_message(f"{parsed_message['DISPLAY_NAME']} is {parsed_message['STATUS']}")
        # If the message is of an unrecognized type
        else:
            log_message("Received an unrecognized message.")
