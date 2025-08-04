# protocol/message_parser.py
from custom_logging.logger import log_message

def parse_message(raw_message):
    """
    Parse a raw LSNP message into a dictionary.
    Expected format:
        TYPE: <value>
        KEY: <value>
        ...
    Returns:
        dict with UPPERCASE keys.
    """
    if not raw_message or not isinstance(raw_message, str):
        log_message("Invalid message format (empty or non-string).")
        return None

    parsed = {}
    lines = raw_message.strip().split("\n")

    for line in lines:
        if ":" not in line:
            log_message(f"Ignoring malformed line: {line}")
            continue
        key, value = line.split(":", 1)
        parsed[key.strip().upper()] = value.strip()

    if "TYPE" not in parsed:
        log_message("Malformed message: Missing TYPE field.")
        return None

    return parsed


def craft_message(msg_type, kv_pairs):
    """
    Create an LSNP message string from a type and key-value dict.
    Ensures TYPE is first, followed by other keys in order provided.
    """
    if not isinstance(kv_pairs, dict):
        raise ValueError("kv_pairs must be a dictionary.")

    # Start with TYPE
    lines = [f"TYPE: {msg_type.upper()}"]

    # Append provided key-value pairs
    for k, v in kv_pairs.items():
        lines.append(f"{k}: {v}")

    return "\n".join(lines) + "\n"


def validate_message(parsed):
    """
    Validate LSNP message based on TYPE.
    """
    if not parsed or "TYPE" not in parsed:
        return False

    msg_type = parsed["TYPE"].upper()

    required_fields = {
        "PING": ["FROM"],
        "POST": ["FROM", "CONTENT"],
        "DM": ["FROM", "TO", "CONTENT"],
        "HELLO": ["USERNAME", "IP", "PORT"],
        "ACK": ["SERVER", "STATUS", "YOUR_USERNAME"],
        "MESSAGE": ["FROM", "CONTENT"],
        "RESPONSE": ["FROM", "CONTENT"]
    }

    if msg_type not in required_fields:
        log_message(f"Unknown message TYPE: {msg_type}")
        return False

    for field in required_fields[msg_type]:
        if field not in parsed:
            log_message(f"Missing required field '{field}' for {msg_type}.")
            return False

    return True


def format_message(parsed):
    """
    Format a parsed dict back into LSNP message string.
    """
    if not parsed:
        return ""
    return "\n".join(f"{k}: {v}" for k, v in parsed.items()) + "\n"
