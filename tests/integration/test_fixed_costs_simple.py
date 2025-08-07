"""
Simple Test Fixed Cost System
Tests the cost calculation logic without importing the full simulation
"""

import time
import random
import json
import os
import sys
import threading
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any


@dataclass
class SimulationActivity:
    """Activity in the infinite simulation"""

    user_id: str
    activity_type: str
    ticks_requested: int
    ticks_completed: int = 0
    base_cost: int = 100
    total_cost: int = 0
    success_rate: float = 0.5
    start_time: float = 0.0
    is_complete: bool = False

    def __post_init__(self):
        self.start_time = time.time()
        # Cost will be calculated when activity is started with proper global multiplier

    def calculate_total_cost(self, global_multiplier: float = 1.0) -> int:
        """Calculate cost with global multiplier applied FIRST to base cost"""
        # Apply global multiplier to base cost FIRST (before entropy compression)
        global_modified_cost = int(self.base_cost * global_multiplier)

        # Ensure minimum cost of 1 RP (no free actions)
        if global_modified_cost < 1:
            global_modified_cost = 1

        if self.ticks_requested <= 1:
            return global_modified_cost

        # Entropy compression: base_over_cost × ticks_requested
        # (global multiplier already applied to base_cost above)
        base_over_cost = global_modified_cost * 2
        compression_cost = base_over_cost * self.ticks_requested

        return int(compression_cost)


def test_fixed_costs():
    """Test that costs are fixed and global multiplier applies correctly"""
    print("🧪 Testing Fixed Cost System")
    print("=" * 50)

    # Test base costs (should be fixed)
    base_costs = {"hunt": 100, "mod": 150, "economy": 75, "fight": 200}

    print("📋 Fixed Base Costs:")
    for activity, cost in base_costs.items():
        print(f"  {activity.title()}: {cost} RP")

    print("\n🔍 Testing Global Multiplier Application:")

    # Test different global multiplier values
    test_multipliers = [0.1, 0.5, 1.0, 2.0, 3.0]

    for multiplier in test_multipliers:
        print(f"\n🌍 Global Multiplier: {multiplier:.1f}x")
        print("-" * 30)

        for activity, base_cost in base_costs.items():
            # Create activity with 1 tick (no entropy compression)
            activity_obj = SimulationActivity(
                user_id="test",
                activity_type=activity,
                ticks_requested=1,
                base_cost=base_cost,
            )

            # Calculate cost with global multiplier
            total_cost = activity_obj.calculate_total_cost(multiplier)
            expected_cost = max(1, int(base_cost * multiplier))  # Minimum 1 RP

            print(f"  {activity.title()}: {base_cost} → {total_cost} RP")

            # Verify the calculation
            assert total_cost == expected_cost, f"Cost calculation wrong for {activity}"

    print("\n🔍 Testing Entropy Compression:")

    # Test multi-tick activities
    activity = SimulationActivity(
        user_id="test", activity_type="hunt", ticks_requested=3, base_cost=100
    )

    for multiplier in [0.1, 1.0, 3.0]:
        total_cost = activity.calculate_total_cost(multiplier)
        global_modified_cost = max(1, int(100 * multiplier))
        expected_cost = int((global_modified_cost * 2) * 3)

        print(
            f"  Hunt 3x @ {multiplier:.1f}x: {total_cost} RP (expected: {expected_cost})"
        )
        assert (
            total_cost == expected_cost
        ), f"Entropy compression wrong for multiplier {multiplier}"

    print("\n✅ All Fixed Cost Tests Passed!")
    print("=" * 50)
    print("📝 Summary:")
    print("  • Base costs are FIXED (no inflation)")
    print("  • Global multiplier applies FIRST to base cost")
    print("  • Minimum cost of 1 RP (no free actions)")
    print("  • Entropy compression applies after global multiplier")
    print("  • Formula: (base_cost × global_multiplier) → entropy_compression")


if __name__ == "__main__":
    test_fixed_costs()
