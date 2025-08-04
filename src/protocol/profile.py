import re
import socket

from typing import Optional
def parse_profile(message: str):
    """Parse PROFILE message in both verbose and non-verbose format."""
    # Verbose format
    verbose_pattern = re.compile(r"USER_ID: (?P<user_id>[\w@\.]+)\nDISPLAY_NAME: (?P<display_name>.+)\nSTATUS: (?P<status>.+)\nAVATAR: (?P<avatar>.+)")
    match = verbose_pattern.match(message)
    if match:
        return match.groupdict()
    # Non-verbose format
    if message.startswith("PROFILE|"):
        parts = message.strip().split("|")
        if len(parts) >= 5:
            return {
                "user_id": parts[1],
                "display_name": parts[2],
                "status": parts[3],
                "avatar": parts[4]
            }
    return None

def send_profile(peer_ip: str, user_id: str, display_name: str, status: str, port: int, avatar: Optional[str] = None, verbose: bool = True):
    """Send a PROFILE message to the peer, now with AVATAR."""
    if avatar is None:
        avatar = "https://example.com/avatar.png"  # Replace with actual avatar logic
    if verbose:
        message = f"TYPE: PROFILE\nUSER_ID: {user_id}\nDISPLAY_NAME: {display_name}\nSTATUS: {status}\nAVATAR: {avatar}\n\n"
    else:
        message = f"PROFILE|{user_id}|{display_name}|{status}|{avatar}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()

# --- Milestone 3: File Transfer Stubs ---
def send_file_offer(peer_ip, filename, filesize, port, verbose=True):
    """Send FILE_OFFER message."""
    if verbose:
        message = f"TYPE: FILE_OFFER\nFILENAME: {filename}\nFILESIZE: {filesize}\n\n"
    else:
        message = f"FILE_OFFER|{filename}|{filesize}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()

def send_file_chunk(peer_ip, filename, chunk_data, chunk_num, port, verbose=True):
    """Send FILE_CHUNK message."""
    if verbose:
        message = f"TYPE: FILE_CHUNK\nFILENAME: {filename}\nCHUNK_NUM: {chunk_num}\nDATA: {chunk_data}\n\n"
    else:
        message = f"FILE_CHUNK|{filename}|{chunk_num}|{chunk_data}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()

def send_file_received(peer_ip, filename, port, verbose=True):
    """Send FILE_RECEIVED message."""
    if verbose:
        message = f"TYPE: FILE_RECEIVED\nFILENAME: {filename}\n\n"
    else:
        message = f"FILE_RECEIVED|{filename}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()

# --- Milestone 3: Token Validation ---
def validate_token(token: str, expected_scope: Optional[str] = None, expiration_seconds: int = 3600):
    """Validate token structure, expiration, and scope."""
    try:
        user, timestamp, scope = token.split("|")
        timestamp = int(timestamp)
        import time
        now = int(time.time())
        if now - timestamp > expiration_seconds:
            return False
        if expected_scope and scope != expected_scope:
            return False
        return True
    except Exception:
        return False

# --- Milestone 3: Group Management Stubs ---
groups = {}

def handle_group_create(group_id, members):
    groups[group_id] = set(members)

def handle_group_update(group_id, members):
    groups[group_id] = set(members)

def print_groups():
    for gid, members in groups.items():
        print(f"Group {gid}: Members: {', '.join(members)}")

def print_group_members(group_id):
    if group_id in groups:
        print(f"Members of {group_id}: {', '.join(groups[group_id])}")
    else:
        print(f"Group {group_id} not found.")

# --- Milestone 3: Game Support (Tic Tac Toe) ---
class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.winner = None

    def make_move(self, pos):
        if self.board[pos] == " " and self.winner is None:
            self.board[pos] = self.current_player
            self.check_winner()
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in wins:
            a,b,c = line
            if self.board[a] == self.board[b] == self.board[c] != " ":
                self.winner = self.board[a]

    def print_board(self):
        print("\n".join([
            "|".join(self.board[i:i+3]) for i in range(0,9,3)
        ]))
        if self.winner:
            print(f"Winner: {self.winner}")
