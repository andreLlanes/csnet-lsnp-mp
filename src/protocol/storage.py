# src/protocol/storage.py
from typing import Dict, List, Set
from datetime import datetime, timedelta

# Existing storage
posts: List[Dict] = []
dms: List[Dict] = []
likes: List[Dict] = []
files: Dict[str, List[bytes]] = {}  # filename -> list of chunks
groups: Dict[str, Set[str]] = {}    # group_id -> set of members
group_messages: List[Dict] = []
valid_messages: List[Dict] = []

# New storage
avatars: Dict[str, bytes] = {}      # user_id -> avatar bytes
tokens: List[Dict] = []             # list of token dicts
games: Dict[str, Dict] = {}         # game_id -> {board, players, moves, winner}

def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")  # Local time AM/PM

# ---------- POSTS / DMS ----------
def store_post(post):
    post["timestamp"] = _timestamp()
    posts.append(post)

def store_dm(dm):
    dm["timestamp"] = _timestamp()
    dms.append(dm)

# ---------- LIKES ----------
def store_like(like):
    likes.append(like)

def print_likes():
    if not likes:
        print("No likes yet.")
        return
    for like in likes:
        ts = like.get("timestamp", _timestamp())
        print(f"[{ts}] {like.get('FROM', 'Unknown')} liked post {like.get('POST_ID', '')}")

# ---------- FILES ----------
def store_file_chunk(filename, chunk):
    if filename not in files:
        files[filename] = []
    files[filename].append(chunk)

def reconstruct_file(filename):
    if filename in files:
        return b''.join(files[filename])
    return None

# ---------- AVATARS ----------
def store_avatar(user_id, avatar_bytes):
    avatars[user_id] = avatar_bytes

def get_avatar(user_id):
    return avatars.get(user_id)

# ---------- GROUPS ----------
def store_group(group_id, members):
    groups[group_id] = set(members)

def add_group_member(group_id, member):
    groups.setdefault(group_id, set()).add(member)

def remove_group_member(group_id, member):
    if group_id in groups:
        groups[group_id].discard(member)

def store_group_message(msg):
    msg["timestamp"] = _timestamp()
    group_messages.append(msg)

def print_groups():
    if not groups:
        print("No groups yet.")
        return
    for gid, members in groups.items():
        print(f"Group {gid}: {', '.join(members)}")

def print_group_messages(group_id=None):
    msgs = group_messages if group_id is None else [m for m in group_messages if m.get("GROUP_ID") == group_id]
    if not msgs:
        print("No group messages yet.")
        return
    for msg in msgs:
        ts = msg.get("timestamp", "")
        sender = msg.get("FROM", "Unknown")
        content = msg.get("CONTENT", "")
        gid = msg.get("GROUP_ID", "Unknown")
        print(f"[{ts}] [Group {gid}] {sender}: {content}")

# ---------- TOKENS ----------
def store_token(token_dict):
    tokens.append(token_dict)

def validate_token(token_dict):
    """Validate token structure, expiration, and scope"""
    exp_str = token_dict.get("EXP")
    scope = token_dict.get("SCOPE")
    if not exp_str or not scope:
        return False
    try:
        exp_dt = datetime.strptime(exp_str, "%Y-%m-%d %H:%M:%S")
        if datetime.now() > exp_dt:
            return False
    except ValueError:
        return False
    # scope validation can be expanded
    return True

def store_valid_message(msg):
    valid_messages.append(msg)

# ---------- GAME (TIC TAC TOE) ----------
def create_game(game_id, player_x, player_o):
    games[game_id] = {
        "board": [" "] * 9,
        "players": {"X": player_x, "O": player_o},
        "moves": [],
        "winner": None
    }

def store_game_move(game_id, player_symbol, position):
    game = games.get(game_id)
    if not game or game["winner"]:
        return
    if game["board"][position] == " ":
        game["board"][position] = player_symbol
        game["moves"].append((player_symbol, position))
        check_game_winner(game_id)

def check_game_winner(game_id):
    game = games.get(game_id)
    if not game:
        return
    board = game["board"]
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] != " " and board[a] == board[b] == board[c]:
            game["winner"] = board[a]
            return

def print_game(game_id):
    game = games.get(game_id)
    if not game:
        print("No such game.")
        return
    print(f"Game {game_id}:")
    print_board(game["board"])
    if game["winner"]:
        print(f"Winner: {game['winner']}")

def print_board(board):
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")

# ---------- PRINT HELPERS ----------
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

def print_valid_messages():
    if not valid_messages:
        print("No valid token messages yet.")
        return
    for msg in valid_messages:
        print(msg)