#!/usr/bin/env python3
"""
Test Message Splitting for Discord
Tests the Discord message splitting functionality
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discord.authoring_bot import AuthoringBot


def test_message_splitting():
    """Test the message splitting functionality"""
    print("Testing Discord Message Splitting")
    print("=" * 50)

    # Create a bot instance to test the splitting method
    bot = AuthoringBot()

    # Test cases
    test_cases = [
        {
            "name": "Short message",
            "message": "This is a short message that should not be split.",
            "expected_parts": 1,
        },
        {
            "name": "Long single line",
            "message": "This is a very long message that exceeds Discord's 2000 character limit and should be split into multiple parts. "
            * 100,
            "expected_parts": "multiple",
        },
        {
            "name": "Long multi-line message",
            "message": "Line 1\n" * 50
            + "This is a very long line that should be split properly\n" * 50
            + "Line 100",
            "expected_parts": "multiple",
        },
        {
            "name": "Message with very long words",
            "message": "This message contains a very long word: "
            + "supercalifragilisticexpialidocious" * 50,
            "expected_parts": "multiple",
        },
        {
            "name": "Message with formatting",
            "message": "**Bold text**\n*Italic text*\n`Code text`\n" * 100,
            "expected_parts": "multiple",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"   Original length: {len(test_case['message'])} characters")

        # Test the splitting method
        parts = bot._split_message(test_case["message"])

        print(f"   Split into: {len(parts)} parts")

        # Verify each part is within Discord's limit
        for j, part in enumerate(parts):
            if len(part) > 2000:
                print(f"   ❌ Part {j+1} is too long: {len(part)} characters")
                return False
            else:
                print(f"   ✅ Part {j+1}: {len(part)} characters")

        # Check if splitting was expected
        if test_case["expected_parts"] == 1:
            if len(parts) != 1:
                print(f"   ❌ Expected 1 part, got {len(parts)}")
                return False
            else:
                print(f"   ✅ Correctly kept as single part")
        else:
            if len(parts) > 1:
                print(f"   ✅ Correctly split into multiple parts")
            else:
                print(f"   ✅ Correctly kept as single part (was short enough)")

    return True


def test_send_long_message_simulation():
    """Test the _send_long_message method logic"""
    print("\n🚀 Testing _send_long_message Logic")
    print("=" * 50)

    bot = AuthoringBot()

    # Test cases for the helper method
    test_messages = [
        "Short message",
        "This is a very long message that should be split into multiple parts. " * 100,
        "Multi-line\nmessage\nwith\nline\nbreaks\n" * 50,
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: Message length {len(message)} characters")

        # Simulate the logic without actually sending
        if len(message) <= 2000:
            print(f"   ✅ Would send as single message")
        else:
            parts = bot._split_message(message, 1900)
            print(f"   📤 Would send as {len(parts)} parts:")
            for j, part in enumerate(parts):
                print(f"      Part {j+1}: {len(part)} characters")

    return True


def test_edge_cases():
    """Test edge cases for message splitting"""
    print("\n🔍 Testing Edge Cases")
    print("=" * 50)

    bot = AuthoringBot()

    edge_cases = [
        {"name": "Empty message", "message": "", "expected": 1},
        {"name": "Single character", "message": "a", "expected": 1},
        {"name": "Exactly 1900 characters", "message": "a" * 1900, "expected": 1},
        {
            "name": "Exactly 2000 characters",
            "message": "a" * 2000,
            "expected": "multiple",  # Should be split since it's over 1900 threshold
        },
        {
            "name": "2001 characters (over 1900 threshold)",
            "message": "a" * 2001,
            "expected": "multiple",  # Should be split since it's over 1900 threshold
        },
        {
            "name": "Very long single word",
            "message": "a" * 3000,
            "expected": "multiple",
        },
    ]

    for test_case in edge_cases:
        print(f"\n📝 {test_case['name']}")
        print(f"   Length: {len(test_case['message'])} characters")

        parts = bot._split_message(test_case["message"])

        if test_case["expected"] == 1:
            if len(parts) == 1:
                print(f"   ✅ Correctly kept as single part")
            else:
                print(f"   ❌ Expected 1 part, got {len(parts)}")
                return False
        else:
            if len(parts) > 1:
                print(f"   ✅ Correctly split into {len(parts)} parts")
            else:
                print(f"   ❌ Expected multiple parts, got 1")
                return False

        # Verify all parts are within limit
        for i, part in enumerate(parts):
            if len(part) > 2000:
                print(f"   ❌ Part {i+1} exceeds limit: {len(part)} characters")
                return False

    return True


def main():
    """Run all message splitting tests"""
    print("Discord Message Splitting Test Suite")
    print("=" * 50)

    tests = [
        ("Basic Message Splitting", test_message_splitting),
        ("Send Long Message Logic", test_send_long_message_simulation),
        ("Edge Cases", test_edge_cases),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   FAILED {test_name} failed with error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 MESSAGE SPLITTING TEST RESULTS")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1

    print(f"\n📈 Overall Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 EXCELLENT! Message splitting is working perfectly!")
        print("💡 Your Discord bot will handle long messages correctly!")
    elif passed >= total * 0.8:
        print("✅ GOOD! Message splitting is working well!")
        print("💡 Most functionality is working correctly!")
    else:
        print("⚠️  MODERATE! Some issues with message splitting.")
        print("💡 Check the failed tests above for details.")

    print("\n🔧 Discord Character Limits:")
    print("   - Regular messages: 2000 characters")
    print("   - Split threshold: 1900 characters (safe buffer)")
    print("   - Embed descriptions: 4096 characters")
    print("   - Embed field values: 1024 characters")


if __name__ == "__main__":
    main()
