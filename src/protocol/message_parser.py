import re

def parse_message(message: str):
    parsed_data = {}
    # --- TICTACTOE_INVITE ---
    if message.startswith("TYPE: TICTACTOE_INVITE"):
        match = re.search(r"FROM: (?P<from>.+)\nTO: (?P<to>.+)\nGAMEID: (?P<game_id>.+)\nMESSAGE_ID: (?P<message_id>.+)\nSYMBOL: (?P<symbol>.+)\nTIMESTAMP: (?P<timestamp>\d+)\nTOKEN: (?P<token>.+)", message)
        if match:
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['GAMEID'] = match.group("game_id")
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['SYMBOL'] = match.group("symbol")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("TICTACTOE_INVITE|"):
        parts = message.strip().split("|")
        if len(parts) >= 8:
            parsed_data['FROM'] = parts[1]
            parsed_data['TO'] = parts[2]
            parsed_data['GAMEID'] = parts[3]
            parsed_data['MESSAGE_ID'] = parts[4]
            parsed_data['SYMBOL'] = parts[5]
            parsed_data['TIMESTAMP'] = parts[6]
            parsed_data['TOKEN'] = parts[7]
        return parsed_data

    # --- TICTACTOE_MOVE ---
    if message.startswith("TYPE: TICTACTOE_MOVE"):
        match = re.search(r"FROM: (?P<from>.+)\nTO: (?P<to>.+)\nGAMEID: (?P<game_id>.+)\nMESSAGE_ID: (?P<message_id>.+)\nPOSITION: (?P<position>\d+)\nSYMBOL: (?P<symbol>.+)\nTURN: (?P<turn>\d+)\nTOKEN: (?P<token>.+)", message)
        if match:
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['GAMEID'] = match.group("game_id")
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['POSITION'] = match.group("position")
            parsed_data['SYMBOL'] = match.group("symbol")
            parsed_data['TURN'] = match.group("turn")
            parsed_data['TOKEN'] = match.group("token")
        return parsed_data
    elif message.startswith("TICTACTOE_MOVE|"):
        parts = message.strip().split("|")
        if len(parts) >= 9:
            parsed_data['FROM'] = parts[1]
            parsed_data['TO'] = parts[2]
            parsed_data['GAMEID'] = parts[3]
            parsed_data['MESSAGE_ID'] = parts[4]
            parsed_data['POSITION'] = parts[5]
            parsed_data['SYMBOL'] = parts[6]
            parsed_data['TURN'] = parts[7]
            parsed_data['TOKEN'] = parts[8]
        return parsed_data

    # --- TICTACTOE_RESULT ---
    if message.startswith("TYPE: TICTACTOE_RESULT"):
        match = re.search(r"FROM: (?P<from>.+)\nTO: (?P<to>.+)\nGAMEID: (?P<game_id>.+)\nMESSAGE_ID: (?P<message_id>.+)\nRESULT: (?P<result>.+)\nSYMBOL: (?P<symbol>.+)\nWINNING_LINE: (?P<winning_line>.+)\nTIMESTAMP: (?P<timestamp>\d+)", message)
        if match:
            parsed_data['FROM'] = match.group("from")
            parsed_data['TO'] = match.group("to")
            parsed_data['GAMEID'] = match.group("game_id")
            parsed_data['MESSAGE_ID'] = match.group("message_id")
            parsed_data['RESULT'] = match.group("result")
            parsed_data['SYMBOL'] = match.group("symbol")
            parsed_data['WINNING_LINE'] = match.group("winning_line")
            parsed_data['TIMESTAMP'] = match.group("timestamp")
        return parsed_data
    elif message.startswith("TICTACTOE_RESULT|"):
        parts = message.strip().split("|")
        if len(parts) >= 9:
            parsed_data['FROM'] = parts[1]
            parsed_data['TO'] = parts[2]
            parsed_data['GAMEID'] = parts[3]
            parsed_data['MESSAGE_ID'] = parts[4]
            parsed_data['RESULT'] = parts[5]
            parsed_data['SYMBOL'] = parts[6]
            parsed_data['WINNING_LINE'] = parts[7]
            parsed_data['TIMESTAMP'] = parts[8]
        return parsed_data
    # --- Milestone 3: File Transfer ---
    if message.startswith("TYPE: FILE_OFFER"):
        match = re.search(r"FILENAME: (?P<filename>.+)\nFILESIZE: (?P<filesize>\d+)", message)
        if match:
            parsed_data['FILENAME'] = match.group("filename")
            parsed_data['FILESIZE'] = match.group("filesize")
        return parsed_data
    elif message.startswith("FILE_OFFER|"):
        parts = message.strip().split("|")
        if len(parts) >= 3:
            parsed_data['FILENAME'] = parts[1]
            parsed_data['FILESIZE'] = parts[2]
        return parsed_data

    if message.startswith("TYPE: FILE_CHUNK"):
        match = re.search(r"FILENAME: (?P<filename>.+)\nCHUNK_NUM: (?P<chunk_num>\d+)\nDATA: (?P<data>.+)", message)
        if match:
            parsed_data['FILENAME'] = match.group("filename")
            parsed_data['CHUNK_NUM'] = match.group("chunk_num")
            parsed_data['DATA'] = match.group("data")
        return parsed_data
    elif message.startswith("FILE_CHUNK|"):
        parts = message.strip().split("|")
        if len(parts) >= 4:
            parsed_data['FILENAME'] = parts[1]
            parsed_data['CHUNK_NUM'] = parts[2]
            parsed_data['DATA'] = parts[3]
        return parsed_data

    if message.startswith("TYPE: FILE_RECEIVED"):
        match = re.search(r"FILENAME: (?P<filename>.+)", message)
        if match:
            parsed_data['FILENAME'] = match.group("filename")
        return parsed_data
    elif message.startswith("FILE_RECEIVED|"):
        parts = message.strip().split("|")
        if len(parts) >= 2:
            parsed_data['FILENAME'] = parts[1]
        return parsed_data

    # --- Milestone 3: Group Management ---
    if message.startswith("TYPE: GROUP_CREATE"):
        match = re.search(r"GROUP_ID: (?P<group_id>.+)\nMEMBERS: (?P<members>.+)", message)
        if match:
            parsed_data['GROUP_ID'] = match.group("group_id")
            parsed_data['MEMBERS'] = match.group("members").split(",")
        return parsed_data
    elif message.startswith("GROUP_CREATE|"):
        parts = message.strip().split("|")
        if len(parts) >= 3:
            parsed_data['GROUP_ID'] = parts[1]
            parsed_data['MEMBERS'] = parts[2].split(",")
        return parsed_data

    if message.startswith("TYPE: GROUP_UPDATE"):
        match = re.search(r"GROUP_ID: (?P<group_id>.+)\nMEMBERS: (?P<members>.+)", message)
        if match:
            parsed_data['GROUP_ID'] = match.group("group_id")
            parsed_data['MEMBERS'] = match.group("members").split(",")
        return parsed_data
    elif message.startswith("GROUP_UPDATE|"):
        parts = message.strip().split("|")
        if len(parts) >= 3:
            parsed_data['GROUP_ID'] = parts[1]
            parsed_data['MEMBERS'] = parts[2].split(",")
        return parsed_data

    if message.startswith("TYPE: GROUP_MESSAGE"):
        match = re.search(r"GROUP_ID: (?P<group_id>.+)\nFROM: (?P<from>.+)\nCONTENT: (?P<content>.+)", message)
        if match:
            parsed_data['GROUP_ID'] = match.group("group_id")
            parsed_data['FROM'] = match.group("from")
            parsed_data['CONTENT'] = match.group("content")
        return parsed_data
    elif message.startswith("GROUP_MESSAGE|"):
        parts = message.strip().split("|")
        if len(parts) >= 4:
            parsed_data['GROUP_ID'] = parts[1]
            parsed_data['FROM'] = parts[2]
            parsed_data['CONTENT'] = parts[3]
        return parsed_data

    # --- Milestone 3: Game Support (Tic Tac Toe) ---
    if message.startswith("TYPE: TTT_MOVE"):
        match = re.search(r"GAME_ID: (?P<game_id>.+)\nPLAYER: (?P<player>.+)\nPOS: (?P<pos>\d+)", message)
        if match:
            parsed_data['GAME_ID'] = match.group("game_id")
            parsed_data['PLAYER'] = match.group("player")
            parsed_data['POS'] = match.group("pos")
        return parsed_data
    elif message.startswith("TTT_MOVE|"):
        parts = message.strip().split("|")
        if len(parts) >= 4:
            parsed_data['GAME_ID'] = parts[1]
            parsed_data['PLAYER'] = parts[2]
            parsed_data['POS'] = parts[3]
        return parsed_data

    # --- Milestone 3: Token Storage ---
    # This will be handled in the server/client logic, not parser.
    # parsed_data is already initialized above

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
