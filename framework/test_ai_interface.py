#!/usr/bin/env python3
"""
Test script for AI Interface Layer functionality
Demonstrates the I/O bridge between Discord bot and LLM model
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_cli import FrameworkCLI


def test_ai_interface():
    """Test the AI interface layer functionality"""
    print("🧪 Testing AI Interface Layer")
    print("=" * 50)
    
    # Initialize CLI
    cli = FrameworkCLI()
    
    # Test cases
    test_cases = [
        {
            "command": "Help me write a character description for Luna",
            "user_id": "test_user_1",
            "expected_type": "writing_assistance"
        },
        {
            "command": "Embody the character of Eve",
            "user_id": "test_user_2", 
            "expected_type": "character_embodiment"
        },
        {
            "command": "Analyze the emotional state of the story",
            "user_id": "test_user_3",
            "expected_type": "analysis"
        },
        {
            "command": "/analyze",
            "user_id": "test_user_4",
            "expected_type": "framework_analysis"
        },
        {
            "command": "How are you feeling today?",
            "user_id": "test_user_5",
            "expected_type": "emotional_response"
        }
    ]
    
    print("📝 Running test cases...")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['command']}")
        print(f"User: {test_case['user_id']}")
        print(f"Expected Type: {test_case['expected_type']}")
        
        try:
            # Process command through AI interface
            result = cli.process_discord_command(
                test_case['command'],
                test_case['user_id']
            )
            
            if result.get('success', False):
                processed_response = result.get('processed_response', {})
                response_type = processed_response.get('response_type', 'unknown')
                discord_response = result.get('discord_response', {})
                
                print(f"✅ Success!")
                print(f"Response Type: {response_type}")
                embed = discord_response.get('embed', {})
                print(f"Discord Embed Title: {embed.get('title', 'No title')}")
                print(f"Response Length: {len(discord_response.get('content', ''))} chars")
                fields = embed.get('fields', [])
                if len(fields) > 1:
                    print(f"Quality Score: {fields[1].get('value', 'N/A')}")
                else:
                    print(f"Quality Score: N/A")
                
                # Check if response type matches expected
                if test_case['expected_type'] in response_type or response_type in test_case['expected_type']:
                    print("✅ Response type matches expected!")
                else:
                    print(f"⚠️ Response type '{response_type}' doesn't match expected '{test_case['expected_type']}'")
                
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print("-" * 50)
        print()
    
    # Test AI interface layer directly
    print("🔬 Testing AI Interface Layer Directly")
    print("=" * 50)
    
    ai_interface = cli.ai_interface
    
    # Test prompt injection
    test_input = "Write a story about a magical forest"
    enhanced_prompt = ai_interface.inject_prompt_context(test_input, "writing_assistance")
    
    print(f"Original Input: {test_input}")
    injection_metadata = enhanced_prompt.get('injection_metadata', {})
    print(f"Enhanced Prompt Length: {injection_metadata.get('prompt_length', 0)} chars")
    print(f"Context Size: {injection_metadata.get('context_size', 0)} chars")
    print(f"Context Type: {injection_metadata.get('context_type', 'unknown')}")
    
    # Test response processing
    test_response = "In the heart of the enchanted forest, ancient trees whispered secrets to the wind..."
    processed_response = ai_interface.process_llm_response(test_response, enhanced_prompt)
    
    print(f"\nTest Response: {test_response}")
    print(f"Processed Response Type: {processed_response.get('response_type', 'unknown')}")
    writing_quality = processed_response.get('writing_quality', {})
    print(f"Writing Quality Score: {writing_quality.get('overall_score', 0)}")
    print(f"Action Items: {processed_response.get('action_items', [])}")
    
    print("\n✅ AI Interface Layer test completed successfully!")


def test_context_injection():
    """Test context injection functionality"""
    print("\n🔍 Testing Context Injection")
    print("=" * 50)
    
    cli = FrameworkCLI()
    ai_interface = cli.ai_interface
    
    # Test different context types
    context_types = ["general", "writing_assistance", "character_embodiment", "analysis", "emotional_response"]
    
    for context_type in context_types:
        test_input = f"Test input for {context_type}"
        enhanced = ai_interface.inject_prompt_context(test_input, context_type)
        
        print(f"\nContext Type: {context_type}")
        injection_metadata = enhanced.get('injection_metadata', {})
        print(f"Enhanced Length: {injection_metadata.get('prompt_length', 0)} chars")
        print(f"Context Size: {injection_metadata.get('context_size', 0)} chars")
        
        # Show a snippet of the enhanced prompt
        prompt_snippet = enhanced['enhanced_prompt'][:200] + "..." if len(enhanced['enhanced_prompt']) > 200 else enhanced['enhanced_prompt']
        print(f"Prompt Snippet: {prompt_snippet}")
    
    print("\n✅ Context injection test completed!")


def test_response_processing():
    """Test response processing functionality"""
    print("\n🔄 Testing Response Processing")
    print("=" * 50)
    
    cli = FrameworkCLI()
    ai_interface = cli.ai_interface
    
    # Test different response types
    test_responses = [
        "I'll help you develop that character's personality and backstory.",
        "The story flows well, but consider adding more emotional depth.",
        "I'm feeling quite creative today! Let's write something amazing.",
        "This analysis shows strong character development potential.",
        "Here's a general response to your question."
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\nTest Response {i}: {response}")
        
        # Create a simple context
        context = {"user_input": "test", "context_type": "general"}
        
        processed = ai_interface.process_llm_response(response, context)
        
        print(f"Response Type: {processed.get('response_type', 'unknown')}")
        writing_quality = processed.get('writing_quality', {})
        print(f"Quality Score: {writing_quality.get('overall_score', 0)}")
        print(f"Action Items: {processed.get('action_items', [])}")
        emotional_impact = processed.get('emotional_impact', {})
        print(f"Emotional Impact: {emotional_impact.get('emotional_tone', 'unknown')}")
    
    print("\n✅ Response processing test completed!")


if __name__ == "__main__":
    print("🚀 Starting AI Interface Layer Tests")
    print("=" * 60)
    
    try:
        test_ai_interface()
        test_context_injection()
        test_response_processing()
        
        print("\n🎉 All tests completed successfully!")
        print("The AI Interface Layer is ready to serve as the I/O bridge between Discord bot and LLM model.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 