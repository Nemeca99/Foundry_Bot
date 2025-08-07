#!/usr/bin/env python3
"""
Test script for Character Voice Integration
Tests the integration between voice generator and character embodiment
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import logging
from framework.plugins.voice_generator import VoiceGenerator
from framework.plugins.character_embodiment_engine import (
    CharacterEmbodimentEngine,
    EmbodimentType,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MockFramework:
    """Mock framework for testing"""

    def __init__(self):
        self.config = MockConfig()
        self.character_embodiment_engine = None
        self.voice_generator = None


class MockConfig:
    """Mock config for testing"""

    MODELS_DIR = Path("models")


def test_character_voice_integration():
    """Test the character voice integration"""
    logger.info("Testing Character Voice Integration")

    # Initialize the framework
    framework = MockFramework()

    # Initialize character embodiment engine
    character_engine = CharacterEmbodimentEngine(framework)
    framework.character_embodiment_engine = character_engine

    # Initialize voice generator
    voice_generator = VoiceGenerator(framework)
    framework.voice_generator = voice_generator

    # Test content about Shay
    test_content = """
    Shay sat on a log at the edge of the cliff's edge overlooking the dense forest below her. 
    The wind gently blowing her brilliant ruby red hair as it glitters in the moon light. 
    Shay is a young woman with ruby red hair who stands at the center of the village. 
    Shay cautiously approaches the shopkeeper and gently says "Hello sir." 
    Shay hands the shopkeeper her old beat-up leather sheath and says "I was looking to get a new one. I don't have much to offer."
    Shay empties her pockets only to have a few gold pieces in her hand.
    """

    logger.info("Testing character embodiment extraction...")

    # Extract character profile
    character_profile = character_engine.extract_character_from_content(
        "Shay", test_content
    )

    logger.info(f"Character profile extracted:")
    logger.info(f"Name: {character_profile.name}")
    logger.info(f"Personality traits: {character_profile.personality_traits}")
    logger.info(f"Voice patterns: {character_profile.voice_patterns}")
    logger.info(f"Speech patterns: {character_profile.speech_patterns}")

    # Test character voice generation with embodiment
    logger.info("Testing character voice generation with embodiment...")

    test_dialogue = (
        "Hello sir, I was looking to get a new sheath. I don't have much to offer."
    )

    # Test with character embodiment
    voice_result = voice_generator.generate_character_voice("Shay", test_dialogue)

    logger.info(f"Voice generation result: {voice_result}")

    # Test with personality fallback
    logger.info("Testing character voice generation with personality fallback...")

    voice_result_fallback = voice_generator.generate_character_voice(
        "Shay", test_dialogue, "young woman"
    )

    logger.info(f"Voice generation result (fallback): {voice_result_fallback}")

    # Test voice style determination
    logger.info("Testing voice style determination...")

    voice_style = voice_generator._determine_character_voice_style(character_profile)
    logger.info(f"Determined voice style: {voice_style}")

    # Test dialogue enhancement
    logger.info("Testing dialogue enhancement...")

    enhanced_dialogue = voice_generator._enhance_dialogue_with_character_traits(
        test_dialogue, character_profile
    )
    logger.info(f"Enhanced dialogue: {enhanced_dialogue}")

    logger.info("Character voice integration test completed")


def test_with_real_book_content():
    """Test with real book content from Relic story"""
    logger.info("Testing with real book content...")

    # Initialize the framework
    framework = MockFramework()

    # Initialize character embodiment engine
    character_engine = CharacterEmbodimentEngine(framework)
    framework.character_embodiment_engine = character_engine

    # Initialize voice generator
    voice_generator = VoiceGenerator(framework)
    framework.voice_generator = voice_generator

    # Read real book content
    book_path = Path("Book_Collection/Relic/Chapter_1.txt")
    if book_path.exists():
        with open(book_path, "r", encoding="utf-8") as f:
            book_content = f.read()

        logger.info(f"Loaded {len(book_content)} characters from Chapter 1")

        # Extract Shay's character profile
        character_profile = character_engine.extract_character_from_content(
            "Shay", book_content
        )

        logger.info(f"Extracted character profile for Shay:")
        logger.info(f"Personality traits: {character_profile.personality_traits}")
        logger.info(f"Voice patterns: {character_profile.voice_patterns}")

        # Test voice generation with real character
        test_dialogue = "Hello sir, I was looking to get a new sheath."
        voice_result = voice_generator.generate_character_voice("Shay", test_dialogue)

        logger.info(f"Voice generation with real character: {voice_result}")

    else:
        logger.error(f"Book file not found: {book_path}")


if __name__ == "__main__":
    logger.info("Starting Character Voice Integration Tests")

    try:
        # Test basic functionality
        test_character_voice_integration()

        # Test with real book content
        test_with_real_book_content()

        logger.info("All tests completed successfully!")

    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
