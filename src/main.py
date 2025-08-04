import socket
import threading
import argparse
from custom_logging.logger import set_verbose, log
from parser import parse_message, handle_message
from network.presence import start_presence_broadcast
from protocol.message_parser import craft_message
from protocol.storage import print_posts, print_dms

def listener(sock, peers, posts, dms, username, bind_ip, followers, following):
    while True:
        raw, addr = sock.recvfrom(65535)
        raw_str = raw.decode(errors="ignore")
        log(f"RECV < {raw_str.strip()}", verbose_only=True)

        data = parse_message(raw_str)
        msg_type = data.get("TYPE", "").upper()

        if msg_type == "PING":
            # Auto-respond with PROFILE
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
            handle_message(data, peers, posts, dms, followers, following)

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
    posts = []
    dms = []
    followers = set()
    following = set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.ip, args.listen_port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Start broadcasting PING + PROFILE every 5 mins
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
        args=(sock, peers, posts, dms, args.username, args.ip, followers, following),
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
                if not followers:
                    log("No followers to send this post to.")
                else:
                    for follower in followers:
                        payload = craft_message(
                            msg_type="POST",
                            kv_pairs={
                                "USER_ID": f"{args.username}@{args.ip}",
                                "CONTENT": content
                            }
                        )
                        if "@" in follower:
                            user_part, address_part = follower.split("@", 1)
                            if ":" in address_part:
                                ip, port = address_part.split(":")
                                port = int(port)
                            else:
                                ip = address_part
                                port = args.send_port
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
                    payload = craft_message(
                        msg_type="DM",
                        kv_pairs={
                            "FROM": f"{args.username}@{args.ip}",
                            "TO": to_user,
                            "CONTENT": content
                        }
                    )
                    sock.sendto(payload.encode(), (args.ip, args.send_port))
                    log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/follow "):
                target_user = msg[len("/follow "):].strip()
                following.add(target_user)
                payload = craft_message(
                    msg_type="FOLLOW",
                    kv_pairs={
                        "FROM": f"{args.username}@{args.ip}",
                        "TO": target_user
                    }
                )
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.startswith("/unfollow "):
                target_user = msg[len("/unfollow "):].strip()
                following.discard(target_user)
                payload = craft_message(
                    msg_type="UNFOLLOW",
                    kv_pairs={
                        "FROM": f"{args.username}@{args.ip}",
                        "TO": target_user
                    }
                )
                sock.sendto(payload.encode(), (args.ip, args.send_port))
                log(f"SEND > {payload.strip()}", verbose_only=True)

            elif msg.lower() == "/followers":
                if followers:
                    log("Followers:\n" + "\n".join(followers))
                else:
                    log("No followers yet.")

            elif msg.lower() == "/following":
                if following:
                    log("Following:\n" + "\n".join(following))
                else:
                    log("Not following anyone.")

            elif msg.lower() == "/posts":
                print_posts()

            elif msg.lower() == "/dms":
                print_dms()

            else:
                log("Unknown command. Use /post, /profile, /dm, /follow, /unfollow, /followers, /following, /posts, /dms")

    except KeyboardInterrupt:
        log("Shutting down...")

if __name__ == "__main__":
    main()
