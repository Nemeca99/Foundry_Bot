#!/usr/bin/env python3
"""
Test script to debug framework and plugin loading
"""

import sys
from pathlib import Path

# Add framework to path
framework_dir = Path(__file__).parent / "framework"
sys.path.insert(0, str(framework_dir))

try:
    from framework.framework_tool import get_framework

    print("🔍 Testing framework initialization...")
    framework = get_framework()

    print(f"📋 Available plugins: {list(framework.plugins.keys())}")

    # Test text generation
    print("🧪 Testing text generation...")
    result = framework.generate_text("Hello! How are you?")
    print(f"📝 Text generation result: {result}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
