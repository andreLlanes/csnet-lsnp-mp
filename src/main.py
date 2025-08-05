import socket
import threading
import argparse
import base64
import os
from custom_logging.logger import set_verbose, log
from parser import parse_message, handle_message
from network.presence import start_presence_broadcast
from protocol.message_parser import craft_message
from protocol.storage import (
    print_posts, print_dms, likes, files, groups, group_messages
)

CHUNK_SIZE = 1024  # bytes

def listener(sock, peers, username, bind_ip, followers, following):
    while True:
        raw, addr = sock.recvfrom(65535)
        raw_str = raw.decode(errors="ignore")
        log(f"RECV < {raw_str.strip()}", verbose_only=True)

        data = parse_message(raw_str)
        msg_type = data.get("TYPE", "").upper()

        if msg_type == "PING":
            profile_msg = craft_message(
                msg_type="PROFILE",
                kv_pairs={
                    "USER_ID": f"{username}@{bind_ip}",
                    "DISPLAY_NAME": username,
                    "STATUS": "Hello! I am online."
                }
            )
            sock.sendto(profile_msg.encode("utf-8"), addr)
            log(f"SEND > {profile_msg.strip()}", verbose_only=True)
        else:
            handle_message(data, peers, None, None, followers, following)

def send_file(sock, target_ip, target_port, filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    offer_msg = craft_message(
        msg_type="FILE_OFFER",
        kv_pairs={"FILENAME": filename, "SIZE": str(filesize)}
    )
    sock.sendto(offer_msg.encode(), (target_ip, target_port))
    log(f"SEND > {offer_msg.strip()}", verbose_only=True)

    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            chunk_b64 = base64.b64encode(chunk).decode()
            chunk_msg = craft_message(
                msg_type="FILE_CHUNK",
                kv_pairs={"FILENAME": filename, "CHUNK": chunk_b64}
            )
            sock.sendto(chunk_msg.encode(), (target_ip, target_port))
            log(f"SEND > FILE_CHUNK ({len(chunk)} bytes)", verbose_only=True)

    received_msg = craft_message(
        msg_type="FILE_RECEIVED",
        kv_pairs={"FILENAME": filename}
    )
    sock.sendto(received_msg.encode(), (target_ip, target_port))
    log(f"SEND > {received_msg.strip()}", verbose_only=True)

def main():
    parser = argparse.ArgumentParser(description="LSNP Peer Client")
    parser.add_argument("username", help="Username for LSNP")
    parser.add_argument("ip", help="Local IP to bind")
    parser.add_argument("listen_port", type=int, help="Port to listen on")
    parser.add_argument("send_port", type=int, help="Port to send to")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    set_verbose(args.verbose)

    peers = {}
    followers = set()
    following = set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.ip, args.listen_port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    start_presence_broadcast(
        sock,
        f"{args.username}@{args.ip}",
        args.username,
        "Hello! I am online.",
        "<broadcast>",
        args.send_port,
        interval=300
    )

    threading.Thread(
        target=listener,
        args=(sock, peers, args.username, args.ip, followers, following),
        daemon=True
    ).start()

    log(f"Peer {args.username} started on {args.ip}:{args.listen_port}")

    try:
        while True:
            msg = input("> ").strip()
            if msg.lower() == "/quit":
                break

            elif msg.startswith("/post "):
                content = msg[len("/post "):]
                for follower in followers:
                    payload = craft_message(
                        msg_type="POST",
                        kv_pairs={
                            "USER_ID": f"{args.username}@{args.ip}",
                            "CONTENT": content
                        }
                    )
                    ip, port = follower.split("@")[1], args.send_port
                    sock.sendto(payload.encode(), (ip, port))
                    log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/profile "):
                status = msg[len("/profile "):]
                payload = craft_message(
                    msg_type="PROFILE",
                    kv_pairs={
                        "USER_ID": f"{args.username}@{args.ip}",
                        "DISPLAY_NAME": args.username,
                        "STATUS": status
                    }
                )
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/dm "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    to_user, content = parts[1], parts[2]
                    target_ip = to_user.split("@")[1]
                    payload = craft_message(
                        msg_type="DM",
                        kv_pairs={
                            "FROM": f"{args.username}@{args.ip}",
                            "TO": to_user,
                            "CONTENT": content
                        }
                    )
                    sock.sendto(payload.encode(), (target_ip, args.send_port))
                    log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/follow "):
                target_user = msg[len("/follow "):].strip()
                following.add(target_user)
                target_ip = target_user.split("@")[1]
                payload = craft_message(
                    msg_type="FOLLOW",
                    kv_pairs={
                        "FROM": f"{args.username}@{args.ip}",
                        "TO": target_user
                    }
                )
                sock.sendto(payload.encode(), (target_ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/unfollow "):
                target_user = msg[len("/unfollow "):].strip()
                following.discard(target_user)
                target_ip = target_user.split("@")[1]
                payload = craft_message(
                    msg_type="UNFOLLOW",
                    kv_pairs={
                        "FROM": f"{args.username}@{args.ip}",
                        "TO": target_user
                    }
                )
                sock.sendto(payload.encode(), (target_ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.lower() == "/followers":
                log("Followers:\n" + "\n".join(followers) if followers else "No followers yet.")

            elif msg.lower() == "/following":
                log("Following:\n" + "\n".join(following) if following else "Not following anyone.")

            elif msg.lower() == "/posts":
                print_posts()

            elif msg.lower() == "/dms":
                print_dms()

            elif msg.startswith("/avatar "):
                path = msg[len("/avatar "):]
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        avatar_b64 = base64.b64encode(f.read()).decode()
                    payload = craft_message(
                        msg_type="AVATAR",
                        kv_pairs={
                            "USER_ID": f"{args.username}@{args.ip}",
                            "AVATAR": avatar_b64
                        }
                    )
                    sock.sendto(payload.encode(), (args.ip, args.send_port))
                    log(f"SEND > AVATAR", verbose_only=True)
                else:
                    log("Avatar file not found.")

            elif msg.startswith("/like "):
                post_id = msg[len("/like "):]
                payload = craft_message(
                    msg_type="LIKE",
                    kv_pairs={
                        "USER_ID": f"{args.username}@{args.ip}",
                        "POST_ID": post_id
                    }
                )
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > LIKE", verbose_only=True)

            elif msg.startswith("/sendfile "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    target, filepath = parts[1], parts[2]
                    ip, port = target.split(":")
                    send_file(sock, ip, int(port), filepath)

            elif msg.lower() == "/files":
                if files:
                    log("Files received:\n" + "\n".join(files.keys()))
                else:
                    log("No files received.")

            elif msg.lower() == "/likes":
                if likes:
                    for like in likes:
                        print(like)
                else:
                    log("No likes received.")

            elif msg.lower() == "/groups":
                if groups:
                    for gid, members in groups.items():
                        print(f"{gid}: {', '.join(members)}")
                else:
                    log("No groups joined.")

            elif msg.lower() == "/groupmsgs":
                if group_messages:
                    for gm in group_messages:
                        print(gm)
                else:
                    log("No group messages received.")

            else:
                log("Unknown command.")

    except KeyboardInterrupt:
        log("Shutting down...")

if __name__ == "__main__":
    main()
