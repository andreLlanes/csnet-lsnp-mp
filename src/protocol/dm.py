# protocol/dm.py
import re

def parse_dm(message: str):
    dm_pattern = re.compile(r"FROM: (?P<from>[\w@\.]+)\nTO: (?P<to>[\w@\.]+)\nCONTENT: (?P<content>[\w\s]+)\nTIMESTAMP: (?P<timestamp>\d+)\nMESSAGE_ID: (?P<message_id>[\w\d]+)\nTOKEN: (?P<token>[\w@\.|]+)")
    match = dm_pattern.match(message)
    
    if match:
        return match.groupdict()
    return None
