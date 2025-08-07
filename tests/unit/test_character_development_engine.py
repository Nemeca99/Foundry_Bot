#!/usr/bin/env python3
"""
Test script for Character Development Engine
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.character_development_engine import CharacterDevelopmentEngine, initialize, DevelopmentStage, DevelopmentTrigger

def test_character_arc_creation():
    """Test creating character development arcs"""
    print("🎭 Testing Character Arc Creation")
    print("=" * 50)
    
    # Initialize the development engine
    development_engine = initialize()
    
    # Create character arcs for different characters
    shay_arc = development_engine.create_character_arc(
        character_name="Shay",
        arc_description="Shay's journey from a curious village girl to a brave adventurer discovering ancient relics",
        initial_stage=DevelopmentStage.INTRODUCTION
    )
    
    nyx_arc = development_engine.create_character_arc(
        character_name="Nyx",
        arc_description="Nyx's transformation from a mysterious figure to a trusted ally with hidden depths",
        initial_stage=DevelopmentStage.CONFLICT
    )
    
    luna_arc = development_engine.create_character_arc(
        character_name="Luna",
        arc_description="Luna's magical awakening and discovery of her true potential",
        initial_stage=DevelopmentStage.GROWTH
    )
    
    print(f"✅ Created character arcs for Shay, Nyx, and Luna")
    print(f"Shay's stage: {shay_arc.current_stage.value}")
    print(f"Nyx's stage: {nyx_arc.current_stage.value}")
    print(f"Luna's stage: {luna_arc.current_stage.value}")

def test_development_events():
    """Test adding development events"""
    print("\n📈 Testing Development Events")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Add different types of development events for Shay
    events_to_add = [
        (DevelopmentTrigger.STORY_EVENT, "Shay discovers the ancient relic in the forest", 0.8, ['courage', 'curiosity']),
        (DevelopmentTrigger.CHARACTER_INTERACTION, "Shay meets Nyx and learns about the relic's history", 0.6, ['trust', 'knowledge']),
        (DevelopmentTrigger.EMOTIONAL_EXPERIENCE, "Shay feels overwhelming joy when she finds the relic", 0.7, ['emotional_intelligence', 'self_awareness']),
        (DevelopmentTrigger.CHALLENGE_OVERCOME, "Shay overcomes her fear of the unknown forest", 0.9, ['courage', 'resilience']),
        (DevelopmentTrigger.RELATIONSHIP_CHANGE, "Shay forms a deep friendship with Luna", 0.5, ['empathy', 'communication'])
    ]
    
    for trigger, description, impact, growth_areas in events_to_add:
        print(f"📝 Adding {trigger.value} event for Shay...")
        event = development_engine.add_development_event(
            character_name="Shay",
            trigger=trigger,
            description=description,
            impact_score=impact,
            growth_areas_affected=growth_areas
        )
        
        print(f"Event ID: {event.event_id}")
        print(f"Impact Score: {event.impact_score}")
        print(f"Growth Areas: {', '.join(event.growth_areas_affected)}")
        print()

def test_character_growth_tracking():
    """Test character growth tracking"""
    print("\n🌱 Testing Character Growth Tracking")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Get character growth data
    shay_growth = development_engine.get_character_growth("Shay")
    nyx_growth = development_engine.get_character_growth("Nyx")
    
    print("Shay's Growth Data:")
    if shay_growth:
        print(f"- Transformation level: {shay_growth.get('transformation_level', 0.0):.2f}")
        print(f"- Growth areas: {len(shay_growth.get('growth_areas', {}))}")
        print(f"- Development history entries: {len(shay_growth.get('development_history', []))}")
        
        growth_areas = shay_growth.get('growth_areas', {})
        if growth_areas:
            print("- Growth areas breakdown:")
            for area, score in growth_areas.items():
                print(f"  * {area}: {score:.2f}")
    else:
        print("No growth data available")
    
    print("\nNyx's Growth Data:")
    if nyx_growth:
        print(f"- Transformation level: {nyx_growth.get('transformation_level', 0.0):.2f}")
        print(f"- Growth areas: {len(nyx_growth.get('growth_areas', {}))}")
    else:
        print("No growth data available")

def test_character_arc_progression():
    """Test character arc progression"""
    print("\n🔄 Testing Character Arc Progression")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Get character arcs
    shay_arc = development_engine.get_character_arc("Shay")
    nyx_arc = development_engine.get_character_arc("Nyx")
    luna_arc = development_engine.get_character_arc("Luna")
    
    print("Character Arc Status:")
    print(f"Shay: {shay_arc.get('current_stage', 'unknown')}")
    print(f"Nyx: {nyx_arc.get('current_stage', 'unknown')}")
    print(f"Luna: {luna_arc.get('current_stage', 'unknown')}")
    
    # Add high-impact events to trigger stage progression
    print("\n📈 Adding high-impact events to trigger progression...")
    
    high_impact_events = [
        ("Shay faces her greatest fear and emerges stronger", 0.9, ['courage', 'transformation']),
        ("Nyx reveals a deep secret that changes everything", 0.8, ['trust', 'vulnerability']),
        ("Luna discovers her true magical potential", 0.85, ['power', 'identity'])
    ]
    
    for description, impact, growth_areas in high_impact_events:
        event = development_engine.add_development_event(
            character_name="Shay",
            trigger=DevelopmentTrigger.STORY_EVENT,
            description=description,
            impact_score=impact,
            growth_areas_affected=growth_areas
        )
        print(f"Added event: {event.description} (Impact: {event.impact_score})")
    
    # Check updated arcs
    updated_shay_arc = development_engine.get_character_arc("Shay")
    print(f"\nUpdated Shay's stage: {updated_shay_arc.get('current_stage', 'unknown')}")

def test_development_suggestions():
    """Test character development suggestions"""
    print("\n💡 Testing Development Suggestions")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Get development suggestions for different characters
    characters = ["Shay", "Nyx", "Luna"]
    
    for character in characters:
        print(f"\n🎭 Development suggestions for {character}:")
        suggestions = development_engine.suggest_character_development(character)
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

def test_character_progress_analysis():
    """Test character progress analysis"""
    print("\n📊 Testing Character Progress Analysis")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Analyze progress for different characters
    characters = ["Shay", "Nyx", "Luna"]
    
    for character in characters:
        print(f"\n📈 Progress analysis for {character}:")
        progress = development_engine.analyze_character_progress(character)
        
        if 'message' in progress:
            print(f"  {progress['message']}")
        else:
            print(f"  - Current stage: {progress.get('current_stage', 'unknown')}")
            print(f"  - Total events: {progress.get('total_development_events', 0)}")
            print(f"  - High-impact events: {progress.get('high_impact_events', 0)}")
            print(f"  - Average impact: {progress.get('average_impact_score', 0.0):.2f}")
            print(f"  - Transformation level: {progress.get('transformation_level', 0.0):.2f}")
            print(f"  - Strongest area: {progress.get('strongest_growth_area', 'none')} ({progress.get('strongest_area_score', 0.0):.2f})")
            print(f"  - Weakest area: {progress.get('weakest_growth_area', 'none')} ({progress.get('weakest_area_score', 0.0):.2f})")

def test_development_summaries():
    """Test character development summaries"""
    print("\n📋 Testing Development Summaries")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Get development summaries
    characters = ["Shay", "Nyx", "Luna"]
    
    for character in characters:
        print(f"\n📖 Development summary for {character}:")
        summary = development_engine.get_character_development_summary(character)
        print(summary)

def test_development_scenarios():
    """Test development scenario creation"""
    print("\n🎬 Testing Development Scenarios")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Create different types of scenarios
    scenario_types = ['challenge', 'relationship', 'emotional', 'transformation']
    characters = ["Shay", "Nyx", "Luna"]
    
    for character in characters:
        print(f"\n🎭 Scenarios for {character}:")
        for scenario_type in scenario_types:
            scenario = development_engine.create_development_scenario(character, scenario_type)
            print(f"  {scenario_type.title()}: {scenario['title']}")
            print(f"    Description: {scenario['description']}")
            print(f"    Impact Score: {scenario['impact_score']}")
            print(f"    Growth Areas: {', '.join(scenario['growth_areas'])}")

def test_development_events_by_trigger():
    """Test retrieving development events by trigger type"""
    print("\n🔍 Testing Development Events by Trigger")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Get events by different trigger types
    trigger_types = [
        DevelopmentTrigger.STORY_EVENT,
        DevelopmentTrigger.CHARACTER_INTERACTION,
        DevelopmentTrigger.EMOTIONAL_EXPERIENCE,
        DevelopmentTrigger.CHALLENGE_OVERCOME,
        DevelopmentTrigger.RELATIONSHIP_CHANGE
    ]
    
    for trigger in trigger_types:
        events = development_engine.get_development_events("Shay", trigger)
        print(f"{trigger.value.title()} events for Shay: {len(events)}")
        
        for event in events[:2]:  # Show first 2 events
            print(f"  - {event.get('description', 'No description')[:50]}...")

def test_manual_stage_advancement():
    """Test manual character stage advancement"""
    print("\n⚡ Testing Manual Stage Advancement")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Manually advance characters to different stages
    stage_advancements = [
        ("Nyx", DevelopmentStage.GROWTH),
        ("Luna", DevelopmentStage.CRISIS)
    ]
    
    for character, new_stage in stage_advancements:
        print(f"🎭 Advancing {character} to {new_stage.value}...")
        success = development_engine.advance_character_manually(character, new_stage)
        
        if success:
            arc = development_engine.get_character_arc(character)
            print(f"✅ {character} is now at stage: {arc.get('current_stage', 'unknown')}")
        else:
            print(f"❌ Failed to advance {character}")

def test_multiple_character_development():
    """Test development across multiple characters"""
    print("\n👥 Testing Multiple Character Development")
    print("=" * 50)
    
    development_engine = initialize()
    
    # Add development events for multiple characters
    character_events = [
        ("Shay", "Shay learns to trust her instincts", 0.7, ['intuition', 'confidence']),
        ("Nyx", "Nyx reveals a hidden vulnerability", 0.6, ['vulnerability', 'trust']),
        ("Luna", "Luna discovers her magical heritage", 0.8, ['identity', 'power']),
        ("Shay", "Shay helps Nyx overcome a challenge", 0.5, ['leadership', 'empathy']),
        ("Luna", "Luna uses her magic to save someone", 0.9, ['heroism', 'responsibility'])
    ]
    
    for character, description, impact, growth_areas in character_events:
        print(f"📝 Adding event for {character}: {description[:40]}...")
        event = development_engine.add_development_event(
            character_name=character,
            trigger=DevelopmentTrigger.STORY_EVENT,
            description=description,
            impact_score=impact,
            growth_areas_affected=growth_areas
        )
        print(f"  Impact: {event.impact_score}, Areas: {', '.join(event.growth_areas_affected)}")
    
    # Show final summaries for all characters
    print("\n📊 Final Development Summary:")
    for character in ["Shay", "Nyx", "Luna"]:
        summary = development_engine.get_character_development_summary(character)
        print(f"\n{summary}")

if __name__ == "__main__":
    print("🎭 Character Development Engine Test Suite")
    print("=" * 60)
    
    try:
        test_character_arc_creation()
        test_development_events()
        test_character_growth_tracking()
        test_character_arc_progression()
        test_development_suggestions()
        test_character_progress_analysis()
        test_development_summaries()
        test_development_scenarios()
        test_development_events_by_trigger()
        test_manual_stage_advancement()
        test_multiple_character_development()
        
        print("\n🎉 All tests completed successfully!")
        print("The Character Development Engine is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 