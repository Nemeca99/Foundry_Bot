#!/usr/bin/env python3
"""
Entropy Compression Economy System Demo
Shows how global multiplier affects compression costs
"""


def calculate_entropy_compression_cost(
    base_cost: int, ticks: int, global_multiplier: float
) -> int:
    """Calculate entropy compression cost with global multiplier"""
    if ticks <= 1:
        return base_cost

    # Base cost for going over 1 tick
    base_over_cost = base_cost * 2

    # Entropy compression: n × global_multiplier
    compression_multiplier = ticks * global_multiplier

    return int(base_over_cost * compression_multiplier)


def main():
    """Demo the entropy compression economy system"""
    print("🌍 ENTROPY COMPRESSION ECONOMY SYSTEM")
    print("=" * 80)
    print("🎯 Global multiplier affects compression costs")
    print("📊 Formula: (Base Cost × 2) × (Ticks × Global Multiplier)")
    print("=" * 80)

    base_costs = {"Hunt": 100, "Mod": 150, "Economy": 75}

    global_multipliers = [
        {"name": "🌪️ Collapse (0.1x)", "value": 0.1, "color": "red"},
        {"name": "📉 Decline (0.5x)", "value": 0.5, "color": "yellow"},
        {"name": "⚖️ Stable (1.0x)", "value": 1.0, "color": "green"},
        {"name": "📈 Growth (2.0x)", "value": 2.0, "color": "blue"},
        {"name": "🚀 Peak (3.0x)", "value": 3.0, "color": "magenta"},
    ]

    for multiplier_info in global_multipliers:
        multiplier = multiplier_info["value"]
        print(f"\n{multiplier_info['name']} (Global Multiplier: {multiplier:.1f}x)")
        print("-" * 60)

        for activity, base_cost in base_costs.items():
            print(f"\n🏹 {activity} Activity (Base: {base_cost} RP):")

            for ticks in range(1, 11):
                cost = calculate_entropy_compression_cost(base_cost, ticks, multiplier)
                raw_cost = base_cost * ticks
                compression_ratio = cost / raw_cost if raw_cost > 0 else 1

                # Color coding based on compression ratio
                if compression_ratio <= 1.5:
                    status = "✅ Efficient"
                elif compression_ratio <= 3.0:
                    status = "⚠️ Moderate"
                else:
                    status = "🔴 Expensive"

                print(
                    f"  {ticks:2d}x ticks: {cost:4d} RP (vs {raw_cost:4d} raw) {status}"
                )

        print()

    print("=" * 80)
    print("💡 Key Insights:")
    print("  • Collapse (0.1x): Compression is CHEAP - world is empty")
    print("  • Stable (1.0x): Normal compression pricing")
    print("  • Peak (3.0x): Compression is EXPENSIVE - world is crowded")
    print("  • Players must monitor global entropy before bulk actions")
    print("  • Creates strategic tension: time-rich vs RP-rich players")
    print("=" * 80)

    # Show strategic scenarios
    print("\n🎮 Strategic Scenarios:")
    print("-" * 60)

    scenarios = [
        {"name": "Collapse Hunter", "multiplier": 0.1, "ticks": 10, "activity": "Hunt"},
        {"name": "Peak Modder", "multiplier": 3.0, "ticks": 5, "activity": "Mod"},
        {
            "name": "Stable Economist",
            "multiplier": 1.0,
            "ticks": 8,
            "activity": "Economy",
        },
    ]

    for scenario in scenarios:
        base_cost = base_costs[scenario["activity"]]
        cost = calculate_entropy_compression_cost(
            base_cost, scenario["ticks"], scenario["multiplier"]
        )
        raw_cost = base_cost * scenario["ticks"]

        print(f"  {scenario['name']}: {scenario['ticks']}x {scenario['activity']}")
        print(f"    Cost: {cost} RP (vs {raw_cost} raw)")
        print(f"    Multiplier: {scenario['multiplier']:.1f}x")
        print()

    print("=" * 80)
    print("🌍 This system makes the world feel ALIVE and CONNECTED!")
    print("Every bulk action affects and is affected by global entropy.")
    print("=" * 80)


if __name__ == "__main__":
    main()
