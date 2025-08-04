import asyncio
import socket
from custom_logging.logger import log_message
from protocol.message_parser import parse_message  # Import parse_message for parsing messages
from protocol.message_sender import send_profile, send_ack  # Import send_profile to respond with PROFILE
from protocol.storage import store_post, store_dm, store_like, store_file_chunk, reconstruct_file, store_group, store_group_message, store_valid_message, print_posts, print_dms, print_likes, print_groups, print_group_members, print_group_messages
from config.settings import RECEIVE_PORT
from config.settings import VERBOSE_MODE

async def receive_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', RECEIVE_PORT))  # Listen on the RECEIVE_PORT
    sock.setblocking(False)
    loop = asyncio.get_event_loop()
    log_message(f"Listening for incoming messages on port {RECEIVE_PORT}...")
    while True:
        data, addr = await loop.sock_recvfrom(sock, 1024)
        if not data:
            log_message("No data received.")
            continue
        message = data.decode()
        if "TYPE: ACK" in message:
            log_message(f"Received ACK message: {message}")
            continue
        parsed_message = parse_message(message)
        log_message(f"Parsed message: {parsed_message}")
        if "TOKEN" in parsed_message:
            from protocol.profile import validate_token
            if validate_token(parsed_message["TOKEN"]):
                store_valid_message(parsed_message)
        # Handle TicTacToe Invite
        if "GAMEID" in parsed_message and "SYMBOL" in parsed_message and "MESSAGE_ID" in parsed_message and "TOKEN" in parsed_message and "FROM" in parsed_message and "TO" in parsed_message and "TICTACTOE_INVITE" in message:
            from protocol.storage import store_ttt_invite, print_ttt_invites
            store_ttt_invite(parsed_message)
            log_message(f"{parsed_message['FROM']} is inviting you to play tic-tac-toe.")
            print_ttt_invites()
        # Handle TicTacToe Move
        elif "GAMEID" in parsed_message and "POSITION" in parsed_message and "SYMBOL" in parsed_message and "TURN" in parsed_message and "TICTACTOE_MOVE" in message:
            from protocol.storage import store_ttt_move, print_ttt_board
            store_ttt_move(parsed_message["GAMEID"], parsed_message["SYMBOL"], parsed_message["POSITION"])
            print_ttt_board(parsed_message["GAMEID"])
        # Handle TicTacToe Result
        elif "GAMEID" in parsed_message and "RESULT" in parsed_message and "TICTACTOE_RESULT" in message:
            from protocol.storage import store_ttt_result, print_ttt_result
            store_ttt_result(parsed_message["GAMEID"], parsed_message["RESULT"])
            print_ttt_result(parsed_message["GAMEID"])
        # Handle PING message
        elif "USER_ID" in parsed_message and "PING" in message:
            if VERBOSE_MODE:
                log_message(f"PING message received: {message}")
            else:
                log_message("")
            await send_profile(addr[0], "gwen@192.168.1.3", "Gwen", "Online", RECEIVE_PORT)
        # Handle POST message
        elif "USER_ID" in parsed_message and "CONTENT" in parsed_message and "POST" in message:
            store_post(parsed_message)
            if VERBOSE_MODE:
                log_message(f"POST message received: {message}")
            else:
                log_message(f"{addr[0]} sent: {parsed_message['CONTENT']}")
        # Handle DM message
        elif "FROM" in parsed_message and "TO" in parsed_message and "DM" in message:
            store_dm(parsed_message)
            if VERBOSE_MODE:
                log_message(f"DM message received: {message}")
            else:
                log_message(f"{parsed_message['FROM']} sent: {parsed_message['CONTENT']}")
            await send_ack(addr[0], parsed_message['MESSAGE_ID'])
        # Handle LIKE message
        elif "FROM" in parsed_message and "TO" in parsed_message and "LIKE" in message:
            store_like(parsed_message)
            if VERBOSE_MODE:
                log_message(f"LIKE message received: {message}")
            else:
                log_message(f"{parsed_message['FROM']} likes your post.")
        # Handle FOLLOW/UNFOLLOW message
        elif "FROM" in parsed_message and "TO" in parsed_message and "TOKEN" in parsed_message:
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
        # Handle FILE_OFFER, FILE_CHUNK, FILE_RECEIVED
        elif "FILENAME" in parsed_message and "FILESIZE" in parsed_message:
            store_file_chunk(parsed_message["FILENAME"], b"")
        elif "FILENAME" in parsed_message and "CHUNK_NUM" in parsed_message and "DATA" in parsed_message:
            store_file_chunk(parsed_message["FILENAME"], parsed_message["DATA"].encode())
        elif "FILENAME" in parsed_message and "FILE_RECEIVED" in message:
            log_message(f"File {parsed_message['FILENAME']} received.")
        elif "GROUP_ID" in parsed_message and "MEMBERS" in parsed_message:
            store_group(parsed_message["GROUP_ID"], parsed_message["MEMBERS"])
        elif "GROUP_ID" in parsed_message and "FROM" in parsed_message and "CONTENT" in parsed_message:
            store_group_message(parsed_message)
        elif "GAME_ID" in parsed_message and "PLAYER" in parsed_message and "POS" in parsed_message:
            log_message(f"TicTacToe move: Game {parsed_message['GAME_ID']}, Player {parsed_message['PLAYER']}, Pos {parsed_message['POS']}")
        else:
            log_message("Received an unrecognized message.")
