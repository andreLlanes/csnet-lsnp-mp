from custom_logging.logger import log

def parse_message(raw: str) -> dict:
    """Parses raw LSNP key-value message into a dict."""
    lines = raw.strip().split("\n")
    data = {}
    for line in lines:
        if ": " in line:
            key, val = line.split(": ", 1)
            data[key.strip()] = val.strip()
    return data

def handle_message(data: dict, peers: dict, posts: list, dms: list, followers: set, following: set):
    """Handles LSNP message display, storage, and follow/unfollow tracking."""
    msg_type = data.get("TYPE", "")

    if msg_type == "PROFILE":
        peers[data["USER_ID"]] = data.get("DISPLAY_NAME", data["USER_ID"])
        log(f"{peers[data['USER_ID']]}: {data.get('STATUS','')}")

    elif msg_type == "POST":
        posts.append(data)
        log(f"{peers.get(data['USER_ID'], data['USER_ID'])}: {data.get('CONTENT','')}")

    elif msg_type == "DM":
        dms.append(data)
        log(f"[DM] {peers.get(data['FROM'], data['FROM'])}: {data.get('CONTENT','')}")

    elif msg_type == "PING":
        pass  # Silent in non-verbose

    elif msg_type == "ACK":
        pass  # Silent in non-verbose

    elif msg_type == "FOLLOW":
        from_user = data.get("FROM", "")
        followers.add(from_user)
        log(f"{from_user} has followed you")

    elif msg_type == "UNFOLLOW":
        from_user = data.get("FROM", "")
        followers.discard(from_user)
        log(f"{from_user} has unfollowed you")

    else:
        log(f"Unknown message type: {msg_type}", verbose_only=True)
