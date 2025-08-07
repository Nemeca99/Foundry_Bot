#!/usr/bin/env python3
"""
Test Tool Use Functionality
Tests the tool manager plugin with LM Studio
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_tool_use():
    """Test tool use functionality"""
    print("🔧 Testing Tool Use Functionality")
    print("=" * 50)

    try:
        # Get framework
        framework = get_framework()
        print("✅ Framework loaded successfully")

        # Check if tool manager is available
        tool_manager = framework.get_plugin("tool_manager")
        if not tool_manager:
            print("❌ Tool manager plugin not found")
            return False

        print("✅ Tool manager plugin loaded")

        # Test available tools
        available_tools = tool_manager.get_available_tools()
        print(f"🔧 Available tools: {', '.join(available_tools)}")

        # Test simple tool call
        print("\n🧪 Testing tool call...")
        test_message = (
            "Create a story outline for a fantasy novel called 'The Crystal Kingdom'"
        )

        result = framework.call_with_tools(test_message)

        if "error" in result:
            print(f"❌ Tool call failed: {result['error']}")
            return False

        print("✅ Tool call successful!")
        print(f"📝 Response type: {result.get('type', 'unknown')}")

        if result.get("type") == "tool_response":
            print("🔧 Tools were used in the response")
            if "tool_results" in result:
                print(f"📊 Number of tools executed: {len(result['tool_results'])}")
                for tool_result in result["tool_results"]:
                    print(
                        f"  - {tool_result['function_name']}: {tool_result['result'].get('message', 'Executed')}"
                    )

        print(f"\n📄 Response content:")
        print("-" * 30)
        print(result.get("content", "No content"))
        print("-" * 30)

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def test_direct_tool_manager():
    """Test tool manager directly"""
    print("\n🔧 Testing Tool Manager Directly")
    print("=" * 50)

    try:
        from framework.plugins.tool_manager import ToolManager
        from framework.framework_tool import get_framework

        framework = get_framework()
        tool_manager = ToolManager(framework)

        print("✅ Tool manager created successfully")

        # Test tool registration
        tools = tool_manager.tools
        print(f"📋 Registered {len(tools)} tools:")
        for tool in tools:
            function_name = tool["function"]["name"]
            description = tool["function"]["description"]
            print(f"  - {function_name}: {description}")

        # Test specific function
        print("\n🧪 Testing create_story_outline function...")
        args = {
            "title": "Test Story",
            "genre": "fantasy",
            "target_length": "novel",
            "main_character": "A young wizard",
            "setting": "A magical academy",
        }

        result = tool_manager._create_story_outline(args)
        print(f"✅ Function result: {result.get('message', 'No message')}")

        return True

    except Exception as e:
        print(f"❌ Error in direct test: {e}")
        return False


if __name__ == "__main__":
    print("Starting Tool Use Tests")
    print("=" * 50)

    # Test 1: Full tool use integration
    success1 = test_tool_use()

    # Test 2: Direct tool manager
    success2 = test_direct_tool_manager()

    print("\n📊 Test Results:")
    print(f"Tool Use Integration: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Direct Tool Manager: {'✅ PASS' if success2 else '❌ FAIL'}")

    if success1 and success2:
        print("\n🎉 All tests passed! Tool use is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
