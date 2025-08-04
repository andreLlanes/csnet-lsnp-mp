# test_protocol.py
import argparse
from protocol.message_parser import craft_message, parse_message, validate_message, format_message

def run_tests(verbose=False):
    tests_passed = 0
    tests_failed = 0

    def check(test_name, condition):
        nonlocal tests_passed, tests_failed
        if condition:
            tests_passed += 1
            if verbose:
                print(f"[PASS] {test_name}")
        else:
            tests_failed += 1
            print(f"[FAIL] {test_name}")

    # --- TEST 1: Craft HELLO message ---
    hello_msg = craft_message("HELLO", {
        "USERNAME": "alice",
        "IP": "127.0.0.1",
        "PORT": "51001"
    })
    parsed_hello = parse_message(hello_msg)
    check("HELLO parse TYPE", parsed_hello.get("TYPE") == "HELLO")
    check("HELLO parse USERNAME", parsed_hello.get("USERNAME") == "alice")
    check("HELLO validation", validate_message(parsed_hello))

    # --- TEST 2: ACK message ---
    ack_msg = craft_message("ACK", {
        "SERVER": "LSNP-Test",
        "STATUS": "Connected",
        "YOUR_USERNAME": "alice"
    })
    parsed_ack = parse_message(ack_msg)
    check("ACK parse TYPE", parsed_ack.get("TYPE") == "ACK")
    check("ACK validation", validate_message(parsed_ack))

    # --- TEST 3: Round-trip consistency ---
    round_trip_msg = format_message(parsed_ack)
    parsed_round_trip = parse_message(round_trip_msg)
    check("Round-trip TYPE preserved", parsed_round_trip.get("TYPE") == parsed_ack.get("TYPE"))
    check("Round-trip SERVER preserved", parsed_round_trip.get("SERVER") == "LSNP-Test")

    # --- TEST 4: Missing required field detection ---
    bad_msg = craft_message("HELLO", {"USERNAME": "bob"})  # Missing IP and PORT
    parsed_bad = parse_message(bad_msg)
    check("HELLO missing field fails validation", not validate_message(parsed_bad))

    # --- Summary ---
    print("\n--- TEST RESULTS ---")
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    if tests_failed == 0:
        print("✅ All tests passed — Protocol compliance OK.")
    else:
        print("❌ Some tests failed. Check details above.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LSNP Protocol Compliance Test Suite")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed test output")
    args = parser.parse_args()

    run_tests(verbose=args.verbose)
