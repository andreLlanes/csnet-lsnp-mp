# src/protocol/storage.py
from typing import Dict, List, Set
from datetime import datetime

posts: List[Dict] = []
dms: List[Dict] = []
likes: List[Dict] = []
files: Dict[str, List[bytes]] = {}  # filename -> list of chunks
groups: Dict[str, Set[str]] = {}    # group_id -> set of members
group_messages: List[Dict] = []
valid_messages: List[Dict] = []

def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")  # Local time AM/PM

def store_post(post):
    post["timestamp"] = _timestamp()
    posts.append(post)

def store_dm(dm):
    dm["timestamp"] = _timestamp()
    dms.append(dm)

def store_like(like):
    likes.append(like)

def store_file_chunk(filename, chunk):
    if filename not in files:
        files[filename] = []
    files[filename].append(chunk)

def reconstruct_file(filename):
    if filename in files:
        return b''.join(files[filename])
    return None

def store_group(group_id, members):
    groups[group_id] = set(members)

def store_group_message(msg):
    group_messages.append(msg)

def store_valid_message(msg):
    valid_messages.append(msg)

def print_posts():
    if not posts:
        print("No posts yet.")
        return
    for post in posts:
        user = post.get("USER_ID", "Unknown")
        content = post.get("CONTENT", "")
        ts = post.get("timestamp", "")
        print(f"[{ts}] {user}: {content}")

def print_dms():
    if not dms:
        print("No DMs yet.")
        return
    for dm in dms:
        sender = dm.get("FROM", "Unknown")
        content = dm.get("CONTENT", "")
        ts = dm.get("timestamp", "")
        print(f"[{ts}] [DM] {sender}: {content}")
