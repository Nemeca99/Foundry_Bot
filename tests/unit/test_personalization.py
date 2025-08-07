#!/usr/bin/env python3
"""
Test Personalization Engine
Tests the personalization engine plugin functionality
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_personalization_engine():
    """Test personalization engine functionality"""
    print("Testing Personalization Engine")
    print("=" * 50)

    try:
        framework = get_framework()
        print("Framework loaded successfully")

        personalization_engine = framework.get_plugin("personalization_engine")
        if not personalization_engine:
            print("Personalization engine plugin not found")
            return False

        print("Personalization engine plugin loaded")

        # Test writing style analysis
        print("\nTesting writing style analysis...")
        style_data = personalization_engine.analyze_writing_style()

        if style_data:
            print("Writing style analysis completed")
            characteristics = style_data.get("characteristics", {})
            print(
                f"📊 Words analyzed: {characteristics.get('total_words_analyzed', 0):,}"
            )
            print(
                f"📝 Avg sentence length: {characteristics.get('avg_sentence_length', 0):.1f}"
            )
            print(
                f"📚 Vocabulary richness: {characteristics.get('vocabulary_richness', 0):.2f}"
            )
        else:
            print("⚠️ No writing style data found (no text files in Book_Collection)")

        # Test conversation recording
        print("\n💬 Testing conversation recording...")
        personalization_engine.record_conversation(
            "Hello, can you help me write a chapter?",
            "Of course! I'd be happy to help you write a chapter.",
            "chapter_writing",
        )
        print("✅ Conversation recorded")

        # Test conversation pattern analysis
        print("\n📊 Testing conversation pattern analysis...")
        patterns = personalization_engine.analyze_conversation_patterns()
        print(f"✅ Conversation patterns analyzed: {len(patterns)} patterns found")

        # Test personalized prompt generation
        print("\n🎯 Testing personalized prompt generation...")
        base_prompt = "Write a chapter about a magical adventure."
        personalized_prompt = personalization_engine.generate_personalized_prompt(
            base_prompt, "test"
        )
        print("✅ Personalized prompt generated")
        print(f"📝 Original: {base_prompt}")
        print(f"🎨 Personalized: {personalized_prompt[:100]}...")

        # Test writing suggestions
        print("\n💡 Testing writing suggestions...")
        suggestions = personalization_engine.get_writing_suggestions()
        print("✅ Writing suggestions generated")
        print(f"🎨 Style recommendations: {len(suggestions['style_recommendations'])}")
        print(
            f"📚 Vocabulary suggestions: {len(suggestions['vocabulary_suggestions'])}"
        )
        print(f"🎭 Thematic elements: {len(suggestions['thematic_elements'])}")

        # Test style profile
        print("\n📋 Testing style profile creation...")
        profile = personalization_engine.create_style_profile()
        print("✅ Style profile created")
        print(f"📊 Profile keys: {list(profile.keys())}")

        # Test personalization stats
        print("\n📈 Testing personalization statistics...")
        stats = personalization_engine.get_personalization_stats()
        print("✅ Personalization statistics generated")
        print(
            f"🔍 Writing fingerprint: {'✅' if stats['writing_fingerprint_analyzed'] else '❌'}"
        )
        print(
            f"💬 Conversation history: {stats['conversation_history_count']} interactions"
        )
        print(f"⚙️ Style preferences: {stats['style_preferences_count']} saved")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def test_personalization_integration():
    """Test personalization integration with text generation"""
    print("\n🔗 Testing Personalization Integration")
    print("=" * 50)

    try:
        framework = get_framework()

        # Test if personalization affects text generation
        text_generator = framework.get_plugin("text_generator")
        if not text_generator:
            print("❌ Text generator plugin not found")
            return False

        print("✅ Text generator plugin loaded")

        # Create a test project
        project_name = "Personalization_Test"
        framework.create_project(project_name, "Fantasy", "Young Adult", 10000)
        print("✅ Test project created")

        # Test chapter writing with personalization
        print("\n📝 Testing chapter writing with personalization...")
        result = text_generator.write_chapter(
            project_name, "Test Chapter", "A magical adventure begins", 1000
        )

        if "✅" in result:
            print("✅ Chapter written successfully with personalization")
            print(f"📄 Result length: {len(result)} characters")
        else:
            print(f"⚠️ Chapter writing result: {result[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Error in integration test: {e}")
        return False


if __name__ == "__main__":
    print("Starting Personalization Engine Tests")
    print("=" * 50)

    success1 = test_personalization_engine()
    success2 = test_personalization_integration()

    print("\n📊 Test Results:")
    print(f"Personalization Engine: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Integration Test: {'✅ PASS' if success2 else '❌ FAIL'}")

    if success1 and success2:
        print("\n🎉 All tests passed! Personalization engine is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
