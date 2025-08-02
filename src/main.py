# main.py
import asyncio
from network.udp_client import start_sending
from network.udp_server import start_receiving
from custom_logging.logger import setup_logging
from config.settings import VERBOSE_MODE

async def main():
    # Set up logging
    setup_logging(VERBOSE_MODE)
    
    # Start sending and receiving messages concurrently
    await asyncio.gather(start_sending(), start_receiving())  # Run both tasks concurrently

if __name__ == "__main__":
    # Use asyncio.run to run the main async function
    asyncio.run(main())
