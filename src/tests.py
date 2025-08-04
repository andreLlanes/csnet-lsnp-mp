from parser import parse_message

def test_parser():
    raw_profile = "TYPE: PROFILE\nUSER_ID: alice@127.0.0.1\nDISPLAY_NAME: Alice\nSTATUS: Hello\n\n"
    profile = parse_message(raw_profile)
    assert profile["TYPE"] == "PROFILE"
    assert profile["USER_ID"] == "alice@127.0.0.1"

    raw_post = "TYPE: POST\nUSER_ID: alice@127.0.0.1\nCONTENT: Hi!\n\n"
    post = parse_message(raw_post)
    assert post["TYPE"] == "POST"

    raw_dm = "TYPE: DM\nFROM: alice@127.0.0.1\nTO: bob@127.0.0.1\nCONTENT: Hey Bob!\n\n"
    dm = parse_message(raw_dm)
    assert dm["TYPE"] == "DM"

    print("✅ All Milestone 1 parser tests passed!")

if __name__ == "__main__":
    test_parser()
