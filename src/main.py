import asyncio
import sys
from network.udp_client import start_sending
from network.udp_server import receive_message
from custom_logging.logger import setup_logging
from config.settings import VERBOSE_MODE

async def main():
    # Set up logging
    setup_logging(VERBOSE_MODE)
    
    # Determine whether to run sending or receiving based on the argument passed to the script
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        print("Running as Sender...")
        await start_sending()
    elif len(sys.argv) > 1 and sys.argv[1] == "receive":
        print("Running as Receiver...")
        await receive_message()
    else:
        print("Please specify 'send' or 'receive' as an argument.")

if __name__ == "__main__":
    # Use asyncio.run to run the main async function
    asyncio.run(main())
