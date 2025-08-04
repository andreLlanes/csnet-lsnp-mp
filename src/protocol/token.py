# src/protocol/token.py
import time
import uuid

ALLOWED_SCOPES = {
    "POST": ["post", "all"],
    "DM": ["dm", "all"],
    "FOLLOW": ["follow", "all"],
    "UNFOLLOW": ["follow", "all"],
    "GROUP_CREATE": ["group", "all"],
    "GROUP_UPDATE": ["group", "all"],
    "GROUP_MESSAGE": ["group", "all"],
    "FILE_OFFER": ["file", "all"],
    "FILE_CHUNK": ["file", "all"],
    "FILE_RECEIVED": ["file", "all"],
    "LIKE": ["like", "all"],
    # 🎯 Added support for Tic Tac Toe / game actions
    "GAME_CREATE": ["game", "all"],
    "GAME_MOVE": ["game", "all"],
    "GAME_RESULT": ["game", "all"]
}

def validate_token_structure(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 4 and all(parts)

def is_token_expired(token: str) -> bool:
    try:
        parts = token.split(".")
        expiry_ts = int(parts[2])
        return time.time() > expiry_ts
    except:
        return True

def has_scope(token: str, msg_type: str) -> bool:
    try:
        parts = token.split(".")
        scope = parts[1].lower()
        return scope in ALLOWED_SCOPES.get(msg_type.upper(), [])
    except:
        return False

def validate_token(token: str, msg_type: str) -> bool:
    return (
        validate_token_structure(token)
        and not is_token_expired(token)
        and has_scope(token, msg_type)
    )

def generate_token(scope: str, lifetime_seconds: int = 3600) -> str:
    """
    Generate a token matching the current validation rules.

    Args:
        scope (str): The scope of the token (e.g., 'post', 'dm', 'follow', 'all').
        lifetime_seconds (int): How long until the token expires, in seconds.

    Returns:
        str: The generated token string.
    """
    # Make sure scope is valid
    valid_scopes = set(s for scopes in ALLOWED_SCOPES.values() for s in scopes)
    if scope.lower() not in valid_scopes:
        raise ValueError(f"Invalid scope: {scope}. Must be one of: {valid_scopes}")

    # Create token parts
    part0 = uuid.uuid4().hex  # random string
    expiry_ts = int(time.time()) + lifetime_seconds
    part3 = uuid.uuid4().hex  # another random string

    # Join into token format
    token = f"{part0}.{scope.lower()}.{expiry_ts}.{part3}"
    return token
