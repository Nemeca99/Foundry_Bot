#!/usr/bin/env python3
"""
Test Writing Assistant Plugin
Tests all Sudowrite-inspired features
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_writing_assistant():
    """Test the writing assistant plugin"""
    print("Testing Writing Assistant Plugin")
    print("=" * 50)

    try:
        # Get framework
        framework = get_framework()
        print("Framework loaded")

        # Get writing assistant plugin
        writing_assistant = framework.get_plugin("writing_assistant")
        if not writing_assistant:
            print("Writing Assistant plugin not found")
            return False

        print("Writing Assistant plugin loaded")

        # Test available tools
        tools = writing_assistant.get_available_tools()
        print(f"Available tools: {', '.join(tools)}")

        # Create a test project
        test_project = framework.create_project(
            "Test Novel", "Fantasy", "Young Adult", 50000
        )
        print("Test project created")

        # Test autocomplete
        print("\nTesting autocomplete...")
        current_text = "The dragon soared over the mountains, its wings catching the golden light of sunset."
        continuation = writing_assistant.autocomplete("Test Novel", current_text)
        print(f"Autocomplete: {continuation[:100]}...")

        # Test expand scene
        print("\nTesting scene expansion...")
        scene_text = "She opened the door and saw the treasure."
        expanded = writing_assistant.expand_scene("Test Novel", scene_text)
        print(f"Scene expansion: {expanded[:100]}...")

        # Test description generation
        print("\nTesting description generation...")
        description = writing_assistant.generate_description(
            "Test Novel", "ancient castle", "medieval fantasy setting"
        )
        print(f"Description: {description[:100]}...")

        # Test rewrite
        print("\nTesting passage rewrite...")
        original_text = "The hero fought bravely against the villain."
        versions = writing_assistant.rewrite_passage("Test Novel", original_text)
        if "error" not in versions:
            print(f"Rewrite versions: {len(versions)} created")
            for style, text in versions.items():
                if text:
                    print(f"   {style}: {text[:50]}...")
        else:
            print(f"Rewrite failed: {versions['error']}")

        # Test dialogue generation
        print("\nTesting dialogue generation...")
        dialogue = writing_assistant.generate_dialogue(
            "Test Novel", ["Hero", "Villain"], "confrontation", "final battle scene"
        )
        print(f"Dialogue: {dialogue[:100]}...")

        # Test brainstorming
        print("\nTesting brainstorming...")
        ideas = writing_assistant.brainstorm_ideas(
            "magic system", "Fantasy", "medieval setting"
        )
        print(f"Brainstormed {len(ideas)} ideas:")
        for idea in ideas[:3]:
            print(f"   • {idea}")

        # Test story canvas
        print("\nTesting story canvas...")
        canvas = writing_assistant.story_canvas("Test Novel")
        if "error" not in canvas:
            print(
                f"Canvas created with {len(canvas.get('plot_points', []))} plot points"
            )
        else:
            print(f"Canvas failed: {canvas['error']}")

        # Test character bible
        print("\nTesting character bible...")
        profile = writing_assistant.character_bible("Aria", "protagonist", "Fantasy")
        print(f"Character bible: {profile[:100]}...")

        # Test world building
        print("\nTesting world building...")
        world = writing_assistant.world_building("Fantasy", "medieval kingdom")
        print(f"World building: {world[:100]}...")

        # Test name generation
        print("\nTesting name generation...")
        names = writing_assistant.name_generator(
            "character", "Fantasy", "medieval", "Nordic"
        )
        print(f"Generated {len(names)} names:")
        for name in names[:3]:
            print(f"   • {name}")

        # Test plot twist generation
        print("\nTesting plot twist generation...")
        current_plot = "Hero must defeat the villain to save the kingdom"
        twists = writing_assistant.plot_twist_generator(current_plot, "Fantasy")
        print(f"Generated {len(twists)} plot twists:")
        for twist in twists[:3]:
            print(f"   • {twist}")

        print("\nAll Writing Assistant tests completed successfully!")
        return True

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_writing_assistant()
    sys.exit(0 if success else 1)
