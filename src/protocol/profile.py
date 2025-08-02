# protocol/profile.py
import re

def parse_profile(message: str):
    profile_pattern = re.compile(r"USER_ID: (?P<user_id>[\w@\.]+)\nDISPLAY_NAME: (?P<display_name>[\w\s]+)\nSTATUS: (?P<status>[\w\s]+)")
    match = profile_pattern.match(message)
    
    if match:
        return match.groupdict()
    return None
