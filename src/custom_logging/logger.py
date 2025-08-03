# logging/logger.py
import logging

# Global logger setup
logger = None

def setup_logging(verbose):
    global logger
    log_level = logging.DEBUG if verbose else logging.INFO  # Set log level based on verbose mode
    logger = logging.getLogger('LSNP')
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

def log_message(message):
    if logger:
        # Use info level for non-verbose and debug for verbose
        if logger.level == logging.DEBUG:
            logger.debug(message)  # Log at DEBUG level for verbose mode
        else:
            logger.info(message) 