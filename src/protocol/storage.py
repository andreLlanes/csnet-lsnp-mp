ttt_invites: list = []
ttt_accepts: list = []
ttt_results: dict = {}  # game_id -> winner

def store_ttt_invite(invite):
    ttt_invites.append(invite)

def store_ttt_accept(accept):
    ttt_accepts.append(accept)

def store_ttt_result(game_id, winner):
    ttt_results[game_id] = winner

def print_ttt_invites():
    for invite in ttt_invites:
        print(invite)

def print_ttt_accepts():
    for accept in ttt_accepts:
        print(accept)

def print_ttt_result(game_id):
    if game_id in ttt_results:
        print(f"Game {game_id} winner: {ttt_results[game_id]}")
    else:
        print(f"Game {game_id} has no result yet.")
from typing import Dict
from protocol.profile import TicTacToe
games: Dict[str, TicTacToe] = {}

def store_ttt_move(game_id, player, pos):
    if game_id not in games:
        games[game_id] = TicTacToe()
    game = games[game_id]
    # Set current player for move
    game.current_player = player
    game.make_move(int(pos))

def print_ttt_board(game_id):
    if game_id in games:
        print(f"Game {game_id} board:")
        games[game_id].print_board()
    else:
        print(f"Game {game_id} not found.")
# src/protocol/storage.py
from typing import Dict, List, Set

posts: List[Dict] = []
dms: List[Dict] = []
likes: List[Dict] = []
files: Dict[str, List[bytes]] = {}  # filename -> list of chunks
groups: Dict[str, Set[str]] = {}    # group_id -> set of members
group_messages: List[Dict] = []
valid_messages: List[Dict] = []

def store_post(post):
    posts.append(post)

def store_dm(dm):
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
    for post in posts:
        print(post)

def print_dms():
    for dm in dms:
        print(dm)

def print_likes():
    for like in likes:
        print(like)

def print_groups():
    for gid, members in groups.items():
        print(f"Group {gid}: Members: {', '.join(members)}")

def print_group_members(group_id):
    if group_id in groups:
        print(f"Members of {group_id}: {', '.join(groups[group_id])}")
    else:
        print(f"Group {group_id} not found.")

def print_group_messages():
    for msg in group_messages:
        print(msg)
