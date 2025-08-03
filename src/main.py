import asyncio
import sys
from network.udp_client import start_sending, send_post, send_dm, send_follow, send_unfollow, send_ack  # Importing the send functions
from network.udp_server import receive_message
from custom_logging.logger import setup_logging
from config.settings import VERBOSE_MODE

async def main():
    # Set up logging
    setup_logging(VERBOSE_MODE)
    
    # Determine whether to run sending or receiving based on the argument passed to the script
    if len(sys.argv) > 1:
        message_type = sys.argv[1].lower()
        
        if message_type == "send":
            # If send argument is passed, send the appropriate message type using start_sending
            if len(sys.argv) > 2:
                msg_type = sys.argv[2].lower()
                peer_ip = "127.0.0.1"  # For local testing
                kwargs = {}
                if msg_type == "post":
                    kwargs["content"] = sys.argv[3] if len(sys.argv) > 3 else "Whatsup!"
                elif msg_type == "dm":
                    kwargs["to_user"] = sys.argv[3] if len(sys.argv) > 3 else "gwen@192.168.1.12"
                    kwargs["content"] = sys.argv[4] if len(sys.argv) > 4 else "Hello Gwen!"
                elif msg_type == "follow" or msg_type == "unfollow":
                    kwargs["to_user"] = sys.argv[3] if len(sys.argv) > 3 else "gwen@192.168.1.10"
                elif msg_type == "profile":
                    kwargs["display_name"] = sys.argv[3] if len(sys.argv) > 3 else "Andre"
                    kwargs["status"] = sys.argv[4] if len(sys.argv) > 4 else "Online"
                elif msg_type == "ack":
                    kwargs["message_id"] = sys.argv[3] if len(sys.argv) > 3 else "f83d2b1c"
                await start_sending(msg_type, peer_ip, **kwargs)
            else:
                print("Please specify a message type after 'send' (e.g., post, dm, ack, etc.)")
                
        elif message_type == "receive":
            # If receive argument is passed, start receiving messages
            await receive_message()

        else:
            print("Invalid argument. Use: send or receive.")

    else:
        print("Please specify 'send' or 'receive' as an argument.")

if __name__ == "__main__":
    # Use asyncio.run to run the main async function
    asyncio.run(main())
