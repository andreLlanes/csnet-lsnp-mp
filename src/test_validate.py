# test_validate.py
import socket
import time
import base64
from protocol.token import generate_token

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000
MY_USER = "bob@127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1.5)

EXPECTED_FIELDS = {
    "PONG": ["USER_ID"],
    "PROFILE_ACK": ["USER_ID", "DISPLAY_NAME"],
    "POST_ACK": ["POST_ID", "STATUS"],
    "DM_ACK": ["FROM", "TO", "STATUS"],
    "FOLLOW_ACK": ["FROM", "TO", "STATUS"],
    "UNFOLLOW_ACK": ["FROM", "TO", "STATUS"],
    "LIKE_ACK": ["POST_ID", "STATUS"],
    "FILE_OFFER_ACK": ["FILENAME", "SIZE", "STATUS"],
    "FILE_CHUNK_ACK": ["FILENAME", "STATUS"],
    "FILE_RECEIVED_ACK": ["FILENAME", "STATUS"],
    "GROUP_CREATE_ACK": ["GROUP_ID", "STATUS"],
    "GROUP_UPDATE_ACK": ["GROUP_ID", "STATUS"],
    "GROUP_MESSAGE_ACK": ["GROUP_ID", "STATUS"],
    "GAME_CREATE_ACK": ["GAME_ID", "STATUS"],
    "GAME_MOVE_ACK": ["GAME_ID", "POSITION", "STATUS"],
    "GAME_RESULT_ACK": ["GAME_ID", "RESULT", "STATUS"],
    "TEST_DONE_ACK": ["STATUS"],
}

def parse_lsnp(msg):
    """Parse LSNP key-value message into a dict."""
    fields = {}
    for line in msg.strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key.strip()] = value.strip()
    return fields

def validate_response(resp_text, expected_type):
    """Check LSNP format and required fields."""
    fields = parse_lsnp(resp_text)

    # TYPE field present
    if "TYPE" not in fields:
        return False, "Missing TYPE in response."

    # TYPE matches expected
    if expected_type != "*" and fields["TYPE"] != expected_type:
        return False, f"Expected TYPE={expected_type}, got TYPE={fields['TYPE']}."

    # Required fields
    if expected_type in EXPECTED_FIELDS:
        for req in EXPECTED_FIELDS[expected_type]:
            if req not in fields:
                return False, f"Missing required field '{req}' in response."

    return True, "OK"

def send_and_expect(message, send_desc, expect_type):
    print(f"[TEST] {send_desc} -> Expecting TYPE={expect_type}")
    sock.sendto(message.encode(), (TARGET_IP, TARGET_PORT))

    try:
        data, _ = sock.recvfrom(4096)
        resp = data.decode(errors="replace")
        ok, reason = validate_response(resp, expect_type)
        if ok:
            print(f"  [PASS] Got valid {expect_type} | {resp.strip()}")
        else:
            print(f"  [FAIL] {reason} | Response: {resp.strip()}")
    except socket.timeout:
        print("  [FAIL] No reply received (timeout).")

    time.sleep(0.3)

def make_msg(msg_type, **fields):
    kv_lines = [f"TYPE: {msg_type}"]
    for k, v in fields.items():
        kv_lines.append(f"{k}: {v}")
    return "\n".join(kv_lines)

def main():
    t_post   = generate_token("post", 3600)
    t_dm     = generate_token("dm", 3600)
    t_follow = generate_token("follow", 3600)
    t_like   = generate_token("like", 3600)
    t_file   = generate_token("file", 3600)
    t_group  = generate_token("group", 3600)
    t_game   = generate_token("game", 3600)

    avatar_b64 = base64.b64encode(b"fakepngdata").decode()

    tests = [
        ("PING", make_msg("PING", USER_ID=MY_USER), "PONG"),
        ("PROFILE", make_msg("PROFILE", USER_ID=MY_USER, DISPLAY_NAME="Bob",
                             STATUS="Hi Alice, I'm Bob.", AVATAR=avatar_b64), "PROFILE_ACK"),
        ("POST", make_msg("POST", USER_ID=MY_USER, CONTENT="Bob here, hello Alice!", TOKEN=t_post), "POST_ACK"),
        ("DM", make_msg("DM", FROM=MY_USER, TO="alice@127.0.0.1", CONTENT="Private message", TOKEN=t_dm), "DM_ACK"),
        ("FOLLOW", make_msg("FOLLOW", FROM=MY_USER, TO="alice@127.0.0.1", TOKEN=t_follow), "FOLLOW_ACK"),
        ("UNFOLLOW", make_msg("UNFOLLOW", FROM=MY_USER, TO="alice@127.0.0.1", TOKEN=t_follow), "UNFOLLOW_ACK"),
        ("LIKE", make_msg("LIKE", USER_ID=MY_USER, POST_ID="1", TOKEN=t_like), "LIKE_ACK"),
        ("FILE_OFFER", make_msg("FILE_OFFER", FILENAME="test.txt", SIZE="11", TOKEN=t_file), "FILE_OFFER_ACK"),
        ("FILE_CHUNK 1", make_msg("FILE_CHUNK", FILENAME="test.txt",
                                  CHUNK=base64.b64encode(b"Hello ").decode(), TOKEN=t_file), "FILE_CHUNK_ACK"),
        ("FILE_CHUNK 2", make_msg("FILE_CHUNK", FILENAME="test.txt",
                                  CHUNK=base64.b64encode(b"World!").decode(), TOKEN=t_file), "FILE_CHUNK_ACK"),
        ("FILE_RECEIVED", make_msg("FILE_RECEIVED", FILENAME="test.txt", TOKEN=t_file), "FILE_RECEIVED_ACK"),
        ("GROUP_CREATE", make_msg("GROUP_CREATE", GROUP_ID="g1",
                                  MEMBERS="bob@127.0.0.1,alice@127.0.0.1", TOKEN=t_group), "GROUP_CREATE_ACK"),
        ("GROUP_UPDATE", make_msg("GROUP_UPDATE", GROUP_ID="g1",
                                  MEMBERS="bob@127.0.0.1,alice@127.0.0.1,charlie@127.0.0.1", TOKEN=t_group), "GROUP_UPDATE_ACK"),
        ("GROUP_MESSAGE", make_msg("GROUP_MESSAGE", GROUP_ID="g1", FROM=MY_USER,
                                   CONTENT="Hello group!", TOKEN=t_group), "GROUP_MESSAGE_ACK"),
        ("GAME_CREATE", make_msg("GAME_CREATE", GAME_ID="ttt1",
                                 PLAYER_X=MY_USER, PLAYER_O="alice@127.0.0.1", TOKEN=t_game), "GAME_CREATE_ACK"),
        ("GAME_MOVE", make_msg("GAME_MOVE", GAME_ID="ttt1", PLAYER=MY_USER,
                               POSITION="0", TOKEN=t_game), "GAME_MOVE_ACK"),
        ("GAME_RESULT", make_msg("GAME_RESULT", GAME_ID="ttt1", RESULT="X wins", TOKEN=t_game), "GAME_RESULT_ACK"),
        ("TEST_DONE", make_msg("TEST_DONE"), "TEST_DONE_ACK"),
    ]

    for desc, msg, expect in tests:
        send_and_expect(msg, desc, expect)

    print("\n[Testing complete]")

if __name__ == "__main__":
    main()
