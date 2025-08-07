#!/usr/bin/env python3
"""
Exponential Scaling Demo
Shows the exponential cost scaling for multiple ticks
"""


def calculate_exponential_cost(base_cost: int, ticks: int) -> int:
    """Calculate exponential cost for multiple ticks"""
    if ticks <= 1:
        return base_cost

    # Base cost for going over 1 tick
    base_over_cost = base_cost * 2

    # Exponential scaling: 1.1^number_of_ticks_over_1
    ticks_over_one = ticks - 1
    exponential_multiplier = 1.1**ticks_over_one

    return int(base_over_cost * exponential_multiplier)


def main():
    """Demo the exponential scaling"""
    print("💰 EXPONENTIAL SCALING DEMO")
    print("=" * 60)
    print("🎯 RP = Time, exponential cost scaling for multiple ticks")
    print("📊 Formula: Base Cost × 2 × (1.1 ^ (ticks - 1))")
    print("=" * 60)

    base_costs = {"Hunt": 100, "Mod": 150, "Economy": 75}

    for activity, base_cost in base_costs.items():
        print(f"\n🏹 {activity} Activity (Base Cost: {base_cost} RP):")
        print("-" * 50)

        for ticks in range(1, 11):
            cost = calculate_exponential_cost(base_cost, ticks)
            multiplier = cost / base_cost

            # Color coding
            if multiplier <= 2:
                color = "green"
            elif multiplier <= 5:
                color = "yellow"
            else:
                color = "red"

            print(f"  {ticks:2d}x ticks: {cost:4d} RP (x{multiplier:.1f})")

        print()

    print("=" * 60)
    print("💡 Key Points:")
    print("  • 1 tick = base cost")
    print("  • 2+ ticks = base cost × 2 × exponential scaling")
    print("  • Exponential scaling: 1.1^(ticks-1)")
    print("  • Even if you succeed on first tick, you pay for all ticks")
    print("  • This prevents spam and encourages strategic thinking")
    print("=" * 60)


if __name__ == "__main__":
    main()
