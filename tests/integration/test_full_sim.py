#!/usr/bin/env python3
"""
Test Full Simulation Import
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔍 Testing imports...")

try:
    # Test mod system import
    sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"
        ),
    )
    from mod_system import (
        ModSystem,
        GlobalRewardMultiplier,
        ModTemplateGenerator,
        ModTemplate,
        PlayerModProfile,
    )

    print("✅ Mod system imported successfully")
except ImportError as e:
    print(f"❌ Mod system import error: {e}")
    sys.exit(1)

try:
    # Test other imports
    import json
    import time
    import random
    import threading
    from datetime import datetime, timedelta
    from typing import Dict, List, Any, Optional
    from dataclasses import dataclass, asdict
    from enum import Enum

    print("✅ All standard imports successful")
except ImportError as e:
    print(f"❌ Standard import error: {e}")
    sys.exit(1)

print("🎉 All imports successful! Full simulation should work.")
print("🚀 Ready to run the complete game experience!")
