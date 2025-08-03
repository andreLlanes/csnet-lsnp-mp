import re

def parse_message(message: str):
    """Parse incoming message into key-value pairs based on message type."""
    parsed_data = {}

    # Verbose format parsing (multi-line)
    if message.startswith("TYPE: PING"):
        match = re.search(r"USER_ID: (?P<user_id>[\w@\.]+)", message)
        if match:
            parsed_data['USER_ID'] = match.group("user_id")
        return parsed_data
    elif message.startswith("PING|"):
        # Non-verbose PING
        parts = message.strip().split("|")
        if len(parts) >= 2:
            parsed_data['USER_ID'] = parts[1]
        return parsed_data

    elif message.startswith("TYPE: POST"):
        match = re.search(r"USER_ID: (?P<user_id>[\w@\.]+)\nCONTENT: (?P<content>.+)\nTTL: (?P<ttl>\d+)\nMESSAGE_ID: (?P<message_id>[\w\d-]+)\nTOKEN: (?P<token>[\w@\.]+\|\d+\|broadcast)", message)
        if match:
            parsed_data['USER_ID'] = match.group("user_id")
            parsed_data['CONTENT'] = match.group("content")
            parsed_data['TTL'] = match.group("ttl")
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("POST|"):
        # Non-verbose POST
        parts = message.strip().split("|")
        if len(parts) >= 8:
            parsed_data['USER_ID'] = parts[1]
            parsed_data['CONTENT'] = parts[2]
            parsed_data['TTL'] = parts[3]
            parsed_data['MESSAGE_ID'] = parts[4]
            parsed_data['TOKEN'] = f"{parts[5]}|{parts[6]}|{parts[7]}"
        return parsed_data

    elif message.startswith("TYPE: DM"):
        match = re.search(r"FROM: (?P<from>[\w@\.]+)\nTO: (?P<to>[\w@\.]+)\nCONTENT: (?P<content>.+)\nTIMESTAMP: (?P<timestamp>\d+)\nMESSAGE_ID: (?P<message_id>[\w\d-]+)\nTOKEN: (?P<token>[\w@\.]+\|\d+\|chat)", message)
        if match:
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['CONTENT'] = match.group("content")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("DM|"):
        # Non-verbose DM
        parts = message.strip().split("|")
        if len(parts) >= 8:
            parsed_data['FROM'] = parts[1]
            parsed_data['TO'] = parts[2]
            parsed_data['CONTENT'] = parts[3]
            parsed_data['TIMESTAMP'] = parts[4]
            parsed_data['MESSAGE_ID'] = parts[5]
            parsed_data['TOKEN'] = f"{parts[6]}|{parts[7]}"
        return parsed_data

    elif message.startswith("TYPE: UNFOLLOW"):
        match = re.search(r"TYPE: UNFOLLOW\nMESSAGE_ID: (?P<message_id>[\w\d-]+)\nFROM: (?P<from>[\w@\.]+)\nTO: (?P<to>[\w@\.]+)\nTIMESTAMP: (?P<timestamp>\d+)\nTOKEN: (?P<token>[\w@\.]+\|\d+\|follow)", message)
        if match:
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("UNFOLLOW|"):
        # Non-verbose UNFOLLOW
        parts = message.strip().split("|")
        if len(parts) >= 8:
            parsed_data['MESSAGE_ID'] = parts[1]
            parsed_data['FROM'] = parts[2]
            parsed_data['TO'] = parts[3]
            parsed_data['TIMESTAMP'] = parts[4]
            parsed_data['TOKEN'] = f"{parts[5]}|{parts[6]}|{parts[7]}"
        return parsed_data

    elif message.startswith("TYPE: FOLLOW"):
        match = re.search(r"TYPE: FOLLOW\nMESSAGE_ID: (?P<message_id>[\w\d-]+)\nFROM: (?P<from>[\w@\.]+)\nTO: (?P<to>[\w@\.]+)\nTIMESTAMP: (?P<timestamp>\d+)\nTOKEN: (?P<token>[\w@\.]+\|\d+\|follow)", message)
        if match:
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("FOLLOW|"):
        # Non-verbose FOLLOW
        parts = message.strip().split("|")
        if len(parts) >= 8:
            parsed_data['MESSAGE_ID'] = parts[1]
            parsed_data['FROM'] = parts[2]
            parsed_data['TO'] = parts[3]
            parsed_data['TIMESTAMP'] = parts[4]
            parsed_data['TOKEN'] = f"{parts[5]}|{parts[6]}|{parts[7]}"
        return parsed_data

    elif message.startswith("TYPE: LIKE"):
        match = re.search(r"FROM: (?P<from>[\w@\.]+)\nTO: (?P<to>[\w@\.]+)\nPOST_TIMESTAMP: (?P<post_timestamp>\d+)\nACTION: (?P<action>\w+)\nTIMESTAMP: (?P<timestamp>\d+)\nTOKEN: (?P<token>[\w@\.]+\|\d+\|broadcast)", message)
        if match:
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['POST_TIMESTAMP'] = match.group("post_timestamp")
            parsed_data['ACTION'] = match.group("action")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("LIKE|"):
        # Non-verbose LIKE
        parts = message.strip().split("|")
        if len(parts) >= 9:
            parsed_data['FROM'] = parts[1]
            parsed_data['TO'] = parts[2]
            parsed_data['POST_TIMESTAMP'] = parts[3]
            parsed_data['ACTION'] = parts[4]
            parsed_data['TIMESTAMP'] = parts[5]
            parsed_data['TOKEN'] = f"{parts[6]}|{parts[7]}|{parts[8]}"
        return parsed_data

    elif message.startswith("TYPE: PROFILE"):
        match = re.search(r"USER_ID: (?P<user_id>[\w@\.]+)\nDISPLAY_NAME: (?P<display_name>.+)\nSTATUS: (?P<status>.+)", message)
        if match:
            parsed_data['USER_ID'] = match.group("user_id")
            parsed_data['DISPLAY_NAME'] = match.group("display_name")
            parsed_data['STATUS'] = match.group("status")
        return parsed_data
    elif message.startswith("PROFILE|"):
        # Non-verbose PROFILE
        parts = message.strip().split("|")
        if len(parts) >= 4:
            parsed_data['USER_ID'] = parts[1]
            parsed_data['DISPLAY_NAME'] = parts[2]
            parsed_data['STATUS'] = parts[3]
        return parsed_data

    elif message.startswith("TYPE: ACK"):
        match = re.search(r"MESSAGE_ID: (?P<message_id>[\w\d-]+)\nSTATUS: (?P<status>\w+)", message)
        if match:
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['STATUS'] = match.group("status")
        return parsed_data
    elif message.startswith("ACK|"):
        # Non-verbose ACK
        parts = message.strip().split("|")
        if len(parts) >= 3:
            parsed_data['MESSAGE_ID'] = parts[1]
            parsed_data['STATUS'] = parts[2]
        return parsed_data

    return parsed_data
