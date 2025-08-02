# protocol/post.py
import re

def parse_post(message: str):
    post_pattern = re.compile(r"USER_ID: (?P<user_id>[\w@\.]+)\nCONTENT: (?P<content>[\w\s]+)\nTTL: (?P<ttl>\d+)\nMESSAGE_ID: (?P<message_id>[\w\d]+)\nTOKEN: (?P<token>[\w@\.|]+)")
    match = post_pattern.match(message)
    
    if match:
        return match.groupdict()
    return None
