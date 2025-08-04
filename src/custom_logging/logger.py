import datetime

VERBOSE = False

def set_verbose(value: bool):
    global VERBOSE
    VERBOSE = value

def log(message: str, verbose_only=False):
    """Logs message depending on verbosity setting."""
    if not verbose_only or VERBOSE:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] {message}")
