import re
import socket

def parse_profile(message: str):
    profile_pattern = re.compile(r"USER_ID: (?P<user_id>[\w@\.]+)\nDISPLAY_NAME: (?P<display_name>[\w\s]+)\nSTATUS: (?P<status>[\w\s]+)")
    match = profile_pattern.match(message)

    if match:
        return match.groupdict()
    return None

def send_profile(peer_ip: str, user_id: str, display_name: str, status: str, port: int):
    """Send a PROFILE message to the peer."""
    message = f"TYPE: PROFILE\nUSER_ID: {user_id}\nDISPLAY_NAME: {display_name}\nSTATUS: {status}\n\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, port))
    sock.close()
