# main.py
import sys
import asyncio
from network.udp_client import start_sending
from network.udp_server import start_receiving
from custom_logging.logger import setup_logging
from config.settings import VERBOSE_MODE

def main():
    # Set up logging
    setup_logging(VERBOSE_MODE)
    
    # Start sending and receiving messages concurrently
    loop = asyncio.get_event_loop()
    loop.create_task(start_sending())
    loop.create_task(start_receiving())
    
    loop.run_forever()

if __name__ == "__main__":
    main()
