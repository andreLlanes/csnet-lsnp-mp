_verbose_mode = False

def set_verbose(value: bool):
    """
    Enables or disables verbose logging.
    """
    global _verbose_mode
    _verbose_mode = value

def log(message: str, verbose_only=False):
    """
    Logs a message to console.
    If verbose_only=True, only logs if verbose mode is enabled.
    """
    if verbose_only and not _verbose_mode:
        return
    from datetime import datetime
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    print(f"{timestamp} {message}")

def log_message(message: str, verbose_only=False):
    """
    Compatibility wrapper for log().
    """
    log(message, verbose_only=verbose_only)