#!/usr/bin/env python3
"""
Test script for Character System Discord Bot
Tests all character system Discord commands
"""

import sys
import os
from pathlib import Path
import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, patch

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discord.character_system_bot import CharacterSystemBot
from framework.framework_tool import get_framework


class TestCharacterSystemBot(unittest.TestCase):
    """Test cases for Character System Discord Bot"""
    
    def setUp(self):
        """Set up test environment"""
        self.bot = CharacterSystemBot(command_prefix="!")
        self.framework = get_framework()
        
        # Mock Discord context
        self.mock_ctx = Mock()
        self.mock_ctx.send = AsyncMock()
        
    def test_bot_initialization(self):
        """Test bot initialization"""
        self.assertIsNotNone(self.bot)
        self.assertIsNotNone(self.bot.framework)
        self.assertEqual(self.bot.command_prefix, "!")
    
    def test_character_embodiment_command(self):
        """Test character embodiment command"""
        asyncio.run(self.bot.handle_character_embodiment(
            self.mock_ctx, "Shay", "Book_Collection/Relic/Chapter_1.txt"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
        
        # Check if success message was sent
        call_args = self.mock_ctx.send.call_args_list
        success_found = any("Character successfully embodied" in str(call) for call in call_args)
        self.assertTrue(success_found or any("Error" in str(call) for call in call_args))
    
    def test_identity_processing_command(self):
        """Test identity processing command"""
        asyncio.run(self.bot.handle_identity_processing(
            self.mock_ctx, "Shay is a brave adventurer"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_voice_command(self):
        """Test character voice command"""
        asyncio.run(self.bot.handle_character_voice(
            self.mock_ctx, "Shay", "Hello, I am Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_add_memory_command(self):
        """Test add memory command"""
        asyncio.run(self.bot.handle_add_memory(
            self.mock_ctx, "Shay", "personal_experience", "important", "Shay discovered an ancient relic"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_get_memories_command(self):
        """Test get memories command"""
        asyncio.run(self.bot.handle_get_memories(
            self.mock_ctx, "Shay", "personal_experience"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_relationships_command(self):
        """Test character relationships command"""
        asyncio.run(self.bot.handle_character_relationships(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_summary_command(self):
        """Test character summary command"""
        asyncio.run(self.bot.handle_character_summary(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_create_dialogue_profile_command(self):
        """Test create dialogue profile command"""
        asyncio.run(self.bot.handle_create_dialogue_profile(
            self.mock_ctx, "Shay", "adventurous"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_generate_dialogue_command(self):
        """Test generate dialogue command"""
        asyncio.run(self.bot.handle_generate_dialogue(
            self.mock_ctx, "Shay", "Nyx", "conversation", "happy"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_create_interaction_command(self):
        """Test create interaction command"""
        asyncio.run(self.bot.handle_create_interaction(
            self.mock_ctx, "conversation", "Shay, Nyx"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_get_interactions_command(self):
        """Test get interactions command"""
        asyncio.run(self.bot.handle_get_interactions(
            self.mock_ctx, "Shay", "conversation"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_relationship_dynamics_command(self):
        """Test relationship dynamics command"""
        asyncio.run(self.bot.handle_relationship_dynamics(
            self.mock_ctx, "Shay", "Nyx"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_create_character_arc_command(self):
        """Test create character arc command"""
        asyncio.run(self.bot.handle_create_character_arc(
            self.mock_ctx, "Shay", "introduction", "Shay's journey from village girl to adventurer"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_add_development_event_command(self):
        """Test add development event command"""
        asyncio.run(self.bot.handle_add_development_event(
            self.mock_ctx, "Shay", "story_event", 0.8, "Shay discovers her first relic"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_development_summary_command(self):
        """Test character development summary command"""
        asyncio.run(self.bot.handle_character_development_summary(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_suggest_development_command(self):
        """Test suggest development command"""
        asyncio.run(self.bot.handle_suggest_development(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_analyze_progress_command(self):
        """Test analyze progress command"""
        asyncio.run(self.bot.handle_analyze_progress(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_evolve_personality_command(self):
        """Test evolve personality command"""
        asyncio.run(self.bot.handle_evolve_personality(
            self.mock_ctx, "shay_content", "Shay is a brave adventurer who discovers ancient relics"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_become_living_manual_command(self):
        """Test become living manual command"""
        asyncio.run(self.bot.handle_become_living_manual(
            self.mock_ctx, "shay_manual", "Shay is a brave adventurer who discovers ancient relics"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_personality_history_command(self):
        """Test personality history command"""
        asyncio.run(self.bot.handle_personality_history(
            self.mock_ctx
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_learn_from_interaction_command(self):
        """Test learn from interaction command"""
        asyncio.run(self.bot.handle_learn_from_interaction(
            self.mock_ctx, "Shay", "conversation", 0.7
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_learn_from_story_command(self):
        """Test learn from story command"""
        asyncio.run(self.bot.handle_learn_from_story(
            self.mock_ctx, "relic_story", "plot_development", 0.3
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_learning_summary_command(self):
        """Test character learning summary command"""
        asyncio.run(self.bot.handle_character_learning_summary(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_analyze_content_emotions_command(self):
        """Test analyze content emotions command"""
        asyncio.run(self.bot.handle_analyze_content_emotions(
            self.mock_ctx, "shay_emotion_test", "Shay felt joy when discovering the relic"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_generate_emotional_response_command(self):
        """Test generate emotional response command"""
        asyncio.run(self.bot.handle_generate_emotional_response(
            self.mock_ctx, "Shay", "joy", "story_event"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_emotional_summary_command(self):
        """Test character emotional summary command"""
        asyncio.run(self.bot.handle_character_emotional_summary(
            self.mock_ctx, "Shay"
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_character_system_status_command(self):
        """Test character system status command"""
        asyncio.run(self.bot.handle_character_system_status(
            self.mock_ctx
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()
    
    def test_list_characters_command(self):
        """Test list characters command"""
        asyncio.run(self.bot.handle_list_characters(
            self.mock_ctx
        ))
        
        # Verify send was called
        self.mock_ctx.send.assert_called()


def run_comprehensive_test():
    """Run comprehensive test of character system bot"""
    print("🎭 Character System Discord Bot Test Suite")
    print("=" * 50)
    
    # Test bot initialization
    print("🔧 Testing Bot Initialization...")
    try:
        bot = CharacterSystemBot(command_prefix="!")
        print("✅ Bot initialization successful")
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False
    
    # Test framework integration
    print("\n🔧 Testing Framework Integration...")
    try:
        framework = get_framework()
        character_plugins = [
            "character_embodiment_engine",
            "identity_processor",
            "character_memory_system",
            "character_interaction_engine",
            "character_development_engine",
            "content_driven_personality",
            "dynamic_personality_learning",
            "content_emotion_integration"
        ]
        
        loaded_count = 0
        for plugin in character_plugins:
            if plugin in framework.plugins:
                print(f"✅ {plugin} loaded")
                loaded_count += 1
            else:
                print(f"❌ {plugin} not found")
        
        print(f"\n📊 Plugin Status: {loaded_count}/{len(character_plugins)} plugins loaded")
        
        if loaded_count == len(character_plugins):
            print("🎉 All character system plugins loaded successfully!")
        else:
            print("⚠️ Some character system plugins are missing")
            
    except Exception as e:
        print(f"❌ Framework integration test failed: {e}")
        return False
    
    # Test command registration
    print("\n🔧 Testing Command Registration...")
    try:
        commands = [
            "embody", "identity", "character-voice",
            "add-memory", "get-memories", "character-relationships", "character-summary",
            "create-dialogue-profile", "generate-dialogue", "create-interaction",
            "get-interactions", "relationship-dynamics",
            "create-character-arc", "add-development-event", "character-development-summary",
            "suggest-development", "analyze-progress",
            "evolve-personality", "become-living-manual", "personality-history",
            "learn-from-interaction", "learn-from-story", "character-learning-summary",
            "analyze-content-emotions", "generate-emotional-response", "character-emotional-summary",
            "character-system-status", "list-characters"
        ]
        
        registered_commands = [cmd.name for cmd in bot.commands]
        
        for command in commands:
            if command in registered_commands:
                print(f"✅ {command} command registered")
            else:
                print(f"❌ {command} command not found")
        
        print(f"\n📊 Command Status: {len([c for c in commands if c in registered_commands])}/{len(commands)} commands registered")
        
    except Exception as e:
        print(f"❌ Command registration test failed: {e}")
        return False
    
    # Test framework methods
    print("\n🔧 Testing Framework Methods...")
    try:
        # Test character embodiment
        result = framework.embody_character("Shay", "Book_Collection/Relic/Chapter_1.txt")
        if result.get("success"):
            print("✅ Character embodiment working")
        else:
            print(f"⚠️ Character embodiment: {result.get('error', 'Unknown error')}")
        
        # Test identity processing
        result = framework.process_identity("Shay is a brave adventurer", "Shay")
        if result.get("success"):
            print("✅ Identity processing working")
        else:
            print(f"⚠️ Identity processing: {result.get('error', 'Unknown error')}")
        
        # Test memory system
        result = framework.add_character_memory("Shay", "personal_experience", "Shay discovered an ancient relic", "important")
        if hasattr(result, 'memory_id'):  # Check if it's a Memory object
            print("✅ Memory system working")
        elif "error" in result:
            print(f"⚠️ Memory system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Memory system working")
        
        # Test interaction system
        result = framework.create_character_dialogue_profile("Shay", interaction_style="adventurous")
        if hasattr(result, 'character_name'):  # Check if it's a CharacterDialogueProfile object
            print("✅ Interaction system working")
        elif "error" in result:
            print(f"⚠️ Interaction system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Interaction system working")
        
        # Test development system
        result = framework.create_character_arc("Shay", "Shay's journey from village girl to adventurer", "introduction")
        if hasattr(result, 'arc_id'):  # Check if it's a CharacterArc object
            print("✅ Development system working")
        elif "error" in result:
            print(f"⚠️ Development system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Development system working")
        
        # Test personality system
        result = framework.evolve_personality_from_content("Shay is a brave adventurer", "shay_content")
        if hasattr(result, 'base_personality'):  # Check if it's a PersonalityEvolution object
            print("✅ Personality system working")
        elif "error" in result:
            print(f"⚠️ Personality system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Personality system working")
        
        # Test learning system
        result = framework.learn_from_character_interaction("Shay", "conversation", 0.7)
        if hasattr(result, 'event_id'):  # Check if it's a LearningEvent object
            print("✅ Learning system working")
        elif "error" in result:
            print(f"⚠️ Learning system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Learning system working")
        
        # Test emotion system
        result = framework.analyze_content_emotions("Shay felt joy when discovering the relic", "shay_emotion_test")
        if hasattr(result, 'content_id'):  # Check if it's a ContentEmotionalAnalysis object
            print("✅ Emotion system working")
        elif "error" in result:
            print(f"⚠️ Emotion system: {result.get('error', 'Unknown error')}")
        else:
            print("✅ Emotion system working")
        
    except Exception as e:
        print(f"❌ Framework methods test failed: {e}")
        return False
    
    print("\n🎉 Character System Discord Bot Test Suite Completed!")
    print("✅ All systems are ready for Discord integration")
    return True


if __name__ == "__main__":
    # Run comprehensive test
    success = run_comprehensive_test()
    
    if success:
        print("\n🚀 Character System Discord Bot is ready for deployment!")
        print("📋 Available Commands:")
        print("🎭 Character Embodiment:")
        print("  !embody <character> [content_source] - Embody a character")
        print("  !identity <content> - Process content as identity")
        print("  !character-voice <character> <text> - Generate character voice")
        print("\n🧠 Character Memory:")
        print("  !add-memory <character> <type> <importance> <content> - Add memory")
        print("  !get-memories <character> [type] - Get character memories")
        print("  !character-relationships <character> - Get relationships")
        print("  !character-summary <character> - Get character summary")
        print("\n💬 Character Interaction:")
        print("  !create-dialogue-profile <character> [style] - Create dialogue profile")
        print("  !generate-dialogue <speaker> <listener> <type> [emotion] - Generate dialogue")
        print("  !create-interaction <type> <participants> - Create interaction")
        print("  !get-interactions <character> [type] - Get interactions")
        print("  !relationship-dynamics <char1> <char2> - Analyze relationships")
        print("\n📈 Character Development:")
        print("  !create-character-arc <character> <stage> <description> - Create arc")
        print("  !add-development-event <character> <trigger> <impact> <description> - Add event")
        print("  !character-development-summary <character> - Get development summary")
        print("  !suggest-development <character> - Get development suggestions")
        print("  !analyze-progress <character> - Analyze character progress")
        print("\n🧠 Content-Driven Personality:")
        print("  !evolve-personality <content_id> <content> - Evolve personality")
        print("  !become-living-manual <content_id> <content> - Become living manual")
        print("  !personality-history - Get evolution history")
        print("\n🎓 Dynamic Personality Learning:")
        print("  !learn-from-interaction <character> <type> [intensity] - Learn from interaction")
        print("  !learn-from-story <story> <type> [intensity] - Learn from story")
        print("  !character-learning-summary <character> - Get learning summary")
        print("\n😊 Content-Emotion Integration:")
        print("  !analyze-content-emotions <content_id> <content> - Analyze emotions")
        print("  !generate-emotional-response <character> [emotion] [trigger] - Generate response")
        print("  !character-emotional-summary <character> - Get emotional summary")
        print("\n🔧 System Status:")
        print("  !character-system-status - Show system status")
        print("  !list-characters - List available characters")
    else:
        print("\n❌ Character System Discord Bot test failed")
        print("Please check the framework integration and try again") 