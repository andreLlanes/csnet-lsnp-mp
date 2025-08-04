import base64
from custom_logging.logger import log
from protocol.token import validate_token, ALLOWED_SCOPES
from protocol.storage import (
    store_post, store_dm, store_like, store_avatar,
    store_file_chunk, reconstruct_file, store_group,
    add_group_member, remove_group_member, store_group_message,
    store_token, store_valid_message, create_game, store_game_move
)

def parse_message(raw_str):
    """Parses LSNP message in key-value format"""
    data = {}
    for line in raw_str.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip().upper()] = val.strip()
    return data

def handle_message(data, peers, posts, dms, followers, following):
    msg_type = data.get("TYPE", "").upper()

    # Token validation for messages in ALLOWED_SCOPES
    if msg_type in ALLOWED_SCOPES:
        token = data.get("TOKEN", "")
        if not validate_token(token, msg_type):
            log(f"[TOKEN VALIDATION] {msg_type} rejected – invalid/expired token: {token}", verbose_only=True)
            log(f"Rejected {msg_type} due to invalid/expired token.")
            return
        else:
            log(f"[TOKEN VALIDATION] {msg_type} accepted – valid token: {token}", verbose_only=True)
            store_valid_message(data)

    # ---- MILESTONE 1 & 2 ----
    if msg_type == "PROFILE":
        user_id = data.get("USER_ID", "")
        display_name = data.get("DISPLAY_NAME", "")
        status = data.get("STATUS", "")
        peers[user_id] = display_name
        log(f"{display_name}: {status}")

    elif msg_type == "POST":
        store_post(data)
        log(f"[{data.get('timestamp')}] {peers.get(data.get('USER_ID'), data.get('USER_ID'))}: {data.get('CONTENT')}")

    elif msg_type == "DM":
        store_dm(data)
        log(f"[{data.get('timestamp')}] [DM] {peers.get(data.get('FROM'), data.get('FROM'))}: {data.get('CONTENT')}")

    elif msg_type == "FOLLOW":
        followers.add(data.get("FROM", ""))
        log(f"{data.get('FROM')} has followed you")

    elif msg_type == "UNFOLLOW":
        followers.discard(data.get("FROM", ""))
        log(f"{data.get('FROM')} has unfollowed you")

    # ---- MILESTONE 3 ----
    elif msg_type == "LIKE":
        store_like(data)
        from_user = data.get("FROM") or data.get("USER_ID", "")
        log(f"{from_user} liked post {data.get('POST_ID')}")

    elif msg_type == "AVATAR":
        user_id = data.get("USER_ID", "")
        avatar_b64 = data.get("AVATAR", "")
        try:
            avatar_bytes = base64.b64decode(avatar_b64)
            store_avatar(user_id, avatar_bytes)
            log(f"Stored avatar for {user_id}")
        except Exception as e:
            log(f"Failed to decode avatar for {user_id}: {e}")

    elif msg_type == "FILE_OFFER":
        from_user = data.get("FROM") or data.get("USER_ID") or "Unknown"
        if from_user == "Unknown" and peers:  # fallback to our own peer ID if available
            from_user = next(iter(peers.keys()))
        log(f"File offer from {from_user}: {data.get('FILENAME')} ({data.get('SIZE')} bytes)")

    elif msg_type == "FILE_CHUNK":
        filename = data.get("FILENAME", "")
        chunk_b64 = data.get("CHUNK", "")
        try:
            chunk_bytes = base64.b64decode(chunk_b64)
            store_file_chunk(filename, chunk_bytes)
            log(f"Stored chunk for {filename}")
        except Exception as e:
            log(f"Failed to store chunk for {filename}: {e}")

    elif msg_type == "FILE_RECEIVED":
        filename = data.get("FILENAME", "")
        file_bytes = reconstruct_file(filename)
        if file_bytes:
            log(f"Reconstructed file {filename}, size {len(file_bytes)} bytes")
        else:
            log(f"No chunks found for {filename}")

    elif msg_type == "GROUP_CREATE":
        gid = data.get("GROUP_ID", "")
        members = data.get("MEMBERS", "").split(",") if data.get("MEMBERS") else []
        store_group(gid, members)
        log(f"Group {gid} created with members: {', '.join(members)}")

    elif msg_type == "GROUP_UPDATE":
        gid = data.get("GROUP_ID", "")
        action = data.get("ACTION", "").upper()
        member = data.get("MEMBER", "")
        if action == "ADD":
            add_group_member(gid, member)
            log(f"Added {member} to group {gid}")
        elif action == "REMOVE":
            remove_group_member(gid, member)
            log(f"Removed {member} from group {gid}")

    elif msg_type == "GROUP_MESSAGE":
        store_group_message(data)
        log(f"[Group {data.get('GROUP_ID')}] {data.get('FROM')}: {data.get('CONTENT')}")

    elif msg_type == "GAME_CREATE":
        create_game(data.get("GAME_ID", ""), data.get("PLAYER_X", ""), data.get("PLAYER_O", ""))
        log(f"Game {data.get('GAME_ID')} created between {data.get('PLAYER_X')} (X) and {data.get('PLAYER_O')} (O)")

    elif msg_type == "GAME_MOVE":
        gid = data.get("GAME_ID", "")
        player = data.get("PLAYER", "")
        pos = int(data.get("POSITION", -1))
        if 0 <= pos <= 8:
            store_game_move(gid, player, pos)
            log(f"Game {gid}: {player} moved to {pos}")
        else:
            log(f"Invalid move position {pos} in game {gid}")

    elif msg_type == "GAME_RESULT":
        log(f"Game {data.get('GAME_ID')} ended with result: {data.get('RESULT')}")

    elif msg_type == "TEST_DONE":
        log("✅ All test messages processed successfully.")

    else:
        log(f"Unknown message type: {msg_type}")
