from custom_logging.logger import log
from protocol import storage
from datetime import datetime

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
        timestamp = datetime.now().strftime("[%Y-%m-%d %I:%M:%S %p]")
        posts.append(data)
        storage.store_post({"timestamp": timestamp, **data})
        log(f"{timestamp} {peers.get(data['USER_ID'], data['USER_ID'])}: {data.get('CONTENT','')}")

    elif msg_type == "DM":
        timestamp = datetime.now().strftime("[%Y-%m-%d %I:%M:%S %p]")
        dms.append(data)
        storage.store_dm({"timestamp": timestamp, **data})
        log(f"{timestamp} [DM] {peers.get(data['FROM'], data['FROM'])}: {data.get('CONTENT','')}")

    elif msg_type == "FOLLOW":
        from_user = data.get("FROM", "")
        followers.add(from_user)
        log(f"{from_user} has followed you")

    elif msg_type == "UNFOLLOW":
        from_user = data.get("FROM", "")
        followers.discard(from_user)
        log(f"{from_user} has unfollowed you")

    elif msg_type == "TEST_DONE":
        log("✅ Milestone 2 test complete!")

    elif msg_type in ("PING", "ACK"):
        pass  # Silent in non-verbose

    else:
        log(f"Unknown message type: {msg_type}", verbose_only=True)
