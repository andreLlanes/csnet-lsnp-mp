# test_ms3.py
import socket
import time
import base64
from protocol.token import generate_token

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000  # Alice's listening port
MY_USER = "bob@127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message(message):
    sock.sendto(message.encode(), (TARGET_IP, TARGET_PORT))
    time.sleep(0.3)

def make_msg(msg_type, **fields):
    kv_lines = [f"TYPE: {msg_type}"]
    for k, v in fields.items():
        kv_lines.append(f"{k}: {v}")
    return "\n".join(kv_lines)

def main():
    # 1️⃣ Generate tokens for each scope
    t_post   = generate_token("post", 3600)
    t_dm     = generate_token("dm", 3600)
    t_follow = generate_token("follow", 3600)
    t_like   = generate_token("like", 3600)
    t_file   = generate_token("file", 3600)
    t_group  = generate_token("group", 3600)
    t_game   = generate_token("game", 3600)

    # 2️⃣ PING
    send_message(make_msg("PING", USER_ID=MY_USER))

    # 3️⃣ PROFILE (with AVATAR base64)
    avatar_png_b64 = base64.b64encode(b"fakepngdata").decode()
    send_message(make_msg(
        "PROFILE",
        USER_ID=MY_USER,
        DISPLAY_NAME="Bob",
        STATUS="Hi Alice, I'm Bob.",
        AVATAR=avatar_png_b64
    ))

    # 4️⃣ POST
    send_message(make_msg(
        "POST",
        USER_ID=MY_USER,
        CONTENT="Bob here, hello Alice!",
        TOKEN=t_post
    ))

    # 5️⃣ DM
    send_message(make_msg(
        "DM",
        FROM=MY_USER,
        TO="alice@127.0.0.1",
        CONTENT="Private message to Alice",
        TOKEN=t_dm
    ))

    # 6️⃣ FOLLOW
    send_message(make_msg(
        "FOLLOW",
        FROM=MY_USER,
        TO="alice@127.0.0.1",
        TOKEN=t_follow
    ))

    # 7️⃣ UNFOLLOW
    send_message(make_msg(
        "UNFOLLOW",
        FROM=MY_USER,
        TO="alice@127.0.0.1",
        TOKEN=t_follow
    ))

    # 8️⃣ LIKE
    send_message(make_msg(
        "LIKE",
        USER_ID=MY_USER,
        POST_ID="1",
        TOKEN=t_like
    ))

    # 9️⃣ FILE_OFFER
    send_message(make_msg(
        "FILE_OFFER",
        FILENAME="test.txt",
        SIZE="11",
        TOKEN=t_file
    ))

    # 🔟 FILE_CHUNK (send 2 chunks)
    chunk1 = base64.b64encode(b"Hello ").decode()
    chunk2 = base64.b64encode(b"World!").decode()
    send_message(make_msg(
        "FILE_CHUNK",
        FILENAME="test.txt",
        CHUNK=chunk1,
        TOKEN=t_file
    ))
    send_message(make_msg(
        "FILE_CHUNK",
        FILENAME="test.txt",
        CHUNK=chunk2,
        TOKEN=t_file
    ))

    # 1️⃣1️⃣ FILE_RECEIVED
    send_message(make_msg(
        "FILE_RECEIVED",
        FILENAME="test.txt",
        TOKEN=t_file
    ))

    # 1️⃣2️⃣ GROUP_CREATE
    send_message(make_msg(
        "GROUP_CREATE",
        GROUP_ID="g1",
        MEMBERS="bob@127.0.0.1,alice@127.0.0.1",
        TOKEN=t_group
    ))

    # 1️⃣3️⃣ GROUP_UPDATE
    send_message(make_msg(
        "GROUP_UPDATE",
        GROUP_ID="g1",
        MEMBERS="bob@127.0.0.1,alice@127.0.0.1,charlie@127.0.0.1",
        TOKEN=t_group
    ))

    # 1️⃣4️⃣ GROUP_MESSAGE
    send_message(make_msg(
        "GROUP_MESSAGE",
        GROUP_ID="g1",
        FROM=MY_USER,
        CONTENT="Hello group!",
        TOKEN=t_group
    ))

    # 1️⃣5️⃣ GAME_CREATE
    send_message(make_msg(
        "GAME_CREATE",
        GAME_ID="ttt1",
        PLAYER_X=MY_USER,
        PLAYER_O="alice@127.0.0.1",
        TOKEN=t_game
    ))

    # 1️⃣6️⃣ GAME_MOVE
    send_message(make_msg(
        "GAME_MOVE",
        GAME_ID="ttt1",
        PLAYER=MY_USER,
        POSITION="0",
        TOKEN=t_game
    ))

    # 1️⃣7️⃣ GAME_RESULT
    send_message(make_msg(
        "GAME_RESULT",
        GAME_ID="ttt1",
        RESULT="X wins",
        TOKEN=t_game
    ))

    # 1️⃣8️⃣ TEST_DONE
    send_message(make_msg("TEST_DONE"))

    print("[Testing complete, waiting for responses...]")

if __name__ == "__main__":
    main()
