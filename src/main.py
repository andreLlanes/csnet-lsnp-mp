
import asyncio
import sys
from network.udp_client import start_sending
from network.udp_server import receive_message
from custom_logging.logger import setup_logging
from config.settings import VERBOSE_MODE

async def cli_loop():
    print("Welcome to LSNP! Type 'help' for commands.")
    peer_ip = "127.0.0.1"  # For local testing
    while True:
        cmd = input("lsnp> ").strip()
        if cmd == "help":
            print("Commands:")
            print("  post <content>")
            print("  dm <to_user> <content>")
            print("  follow <to_user>")
            print("  unfollow <to_user>")
            print("  profile <display_name> <status>")
            print("  ack <message_id>")
            print("  ttt_invite <game_id> <from_user> <to_user> <symbol>")
            print("  ttt_move <game_id> <from_user> <to_user> <message_id> <position> <symbol> <turn>")
            print("  ttt_result <game_id> <from_user> <to_user> <message_id> <result> <symbol> <winning_line> <timestamp>")
            print("  ttt_board <game_id>")
            print("  exit")
        elif cmd.startswith("post "):
            _, content = cmd.split(" ", 1)
            await start_sending("post", peer_ip, content=content)
        elif cmd.startswith("dm "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: dm <to_user> <content>")
                continue
            _, to_user, content = parts
            await start_sending("dm", peer_ip, to_user=to_user, content=content)
        elif cmd.startswith("follow "):
            _, to_user = cmd.split(" ", 1)
            await start_sending("follow", peer_ip, to_user=to_user)
        elif cmd.startswith("unfollow "):
            _, to_user = cmd.split(" ", 1)
            await start_sending("unfollow", peer_ip, to_user=to_user)
        elif cmd.startswith("profile "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: profile <display_name> <status>")
                continue
            _, display_name, status = parts
            await start_sending("profile", peer_ip, display_name=display_name, status=status)
        elif cmd.startswith("ack "):
            _, message_id = cmd.split(" ", 1)
            await start_sending("ack", peer_ip, message_id=message_id)
        elif cmd.startswith("ttt_invite "):
            parts = cmd.split(" ")
            if len(parts) < 5:
                print("Usage: ttt_invite <game_id> <from_user> <to_user> <symbol>")
                continue
            _, game_id, from_user, to_user, symbol = parts
            await start_sending("ttt_invite", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, symbol=symbol)
        elif cmd.startswith("ttt_move "):
            parts = cmd.split(" ")
            if len(parts) < 8:
                print("Usage: ttt_move <game_id> <from_user> <to_user> <message_id> <position> <symbol> <turn>")
                continue
            _, game_id, from_user, to_user, message_id, position, symbol, turn = parts
            await start_sending("ttt_move", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, message_id=message_id, position=position, symbol=symbol, turn=turn)
        elif cmd.startswith("ttt_result "):
            parts = cmd.split(" ")
            if len(parts) < 9:
                print("Usage: ttt_result <game_id> <from_user> <to_user> <message_id> <result> <symbol> <winning_line> <timestamp>")
                continue
            _, game_id, from_user, to_user, message_id, result, symbol, winning_line, timestamp = parts
            await start_sending("ttt_result", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, message_id=message_id, result=result, symbol=symbol, winning_line=winning_line, timestamp=timestamp)
        elif cmd.startswith("ttt_board "):
            parts = cmd.split(" ")
            if len(parts) < 2:
                print("Usage: ttt_board <game_id>")
                continue
            _, game_id = parts
            from protocol.storage import print_ttt_board
            print_ttt_board(game_id)
        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

async def main():
    setup_logging(VERBOSE_MODE)
    # Track if pinging should be enabled
    ping_enabled = True
    # Set peer_ip for local testing
    peer_ip = "127.0.0.1"
    # Start receiver in the background
    receiver_task = asyncio.create_task(receive_message())

    # Start pinging only if enabled
    ping_task = None
    if ping_enabled:
        from network.udp_client import send_ping_periodically, USER_ID
        ping_task = asyncio.create_task(send_ping_periodically(peer_ip, USER_ID, 51000))

    # Custom CLI loop
    print("Welcome to LSNP! Type 'help' for commands.")
    first_command = True
    while True:
        cmd = input("lsnp> ").strip()
        # Disable pinging if first command is a TicTacToe game command
        if first_command and (cmd.startswith("ttt_invite ") or cmd.startswith("ttt_move ") or cmd.startswith("ttt_result ") or cmd.startswith("ttt_board ")):
            if ping_task:
                ping_task.cancel()
            ping_enabled = False
        first_command = False
        if cmd == "help":
            print("Commands:")
            print("  post <content>")
            print("  dm <to_user> <content>")
            print("  follow <to_user>")
            print("  unfollow <to_user>")
            print("  profile <display_name> <status>")
            print("  ack <message_id>")
            print("  ttt_invite <game_id> <from_user> <to_user> <symbol>")
            print("  ttt_move <game_id> <from_user> <to_user> <message_id> <position> <symbol> <turn>")
            print("  ttt_result <game_id> <from_user> <to_user> <message_id> <result> <symbol> <winning_line> <timestamp>")
            print("  ttt_board <game_id>")
            print("  exit")
        elif cmd.startswith("post "):
            _, content = cmd.split(" ", 1)
            await start_sending("post", peer_ip, content=content)
        elif cmd.startswith("dm "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: dm <to_user> <content>")
                continue
            _, to_user, content = parts
            await start_sending("dm", peer_ip, to_user=to_user, content=content)
        elif cmd.startswith("follow "):
            _, to_user = cmd.split(" ", 1)
            await start_sending("follow", peer_ip, to_user=to_user)
        elif cmd.startswith("unfollow "):
            _, to_user = cmd.split(" ", 1)
            await start_sending("unfollow", peer_ip, to_user=to_user)
        elif cmd.startswith("profile "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: profile <display_name> <status>")
                continue
            _, display_name, status = parts
            await start_sending("profile", peer_ip, display_name=display_name, status=status)
        elif cmd.startswith("ack "):
            _, message_id = cmd.split(" ", 1)
            await start_sending("ack", peer_ip, message_id=message_id)
        elif cmd.startswith("ttt_invite "):
            parts = cmd.split(" ")
            if len(parts) < 5:
                print("Usage: ttt_invite <game_id> <from_user> <to_user> <symbol>")
                continue
            _, game_id, from_user, to_user, symbol = parts
            await start_sending("ttt_invite", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, symbol=symbol)
        elif cmd.startswith("ttt_move "):
            parts = cmd.split(" ")
            if len(parts) < 8:
                print("Usage: ttt_move <game_id> <from_user> <to_user> <message_id> <position> <symbol> <turn>")
                continue
            _, game_id, from_user, to_user, message_id, position, symbol, turn = parts
            await start_sending("ttt_move", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, message_id=message_id, position=position, symbol=symbol, turn=turn)
        elif cmd.startswith("ttt_result "):
            parts = cmd.split(" ")
            if len(parts) < 9:
                print("Usage: ttt_result <game_id> <from_user> <to_user> <message_id> <result> <symbol> <winning_line> <timestamp>")
                continue
            _, game_id, from_user, to_user, message_id, result, symbol, winning_line, timestamp = parts
            await start_sending("ttt_result", peer_ip, game_id=game_id, from_user=from_user, to_user=to_user, message_id=message_id, result=result, symbol=symbol, winning_line=winning_line, timestamp=timestamp)
        elif cmd.startswith("ttt_board "):
            parts = cmd.split(" ")
            if len(parts) < 2:
                print("Usage: ttt_board <game_id>")
                continue
            _, game_id = parts
            from protocol.storage import print_ttt_board
            print_ttt_board(game_id)
        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

    # Cancel receiver and ping when CLI exits
    receiver_task.cancel()
    if ping_task:
        ping_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
