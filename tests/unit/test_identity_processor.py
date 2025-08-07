#!/usr/bin/env python3
"""
Test script for Identity Processor Plugin
Tests the revolutionary "I AM" transformation with Shay from Relic story
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import logging
from framework.plugins.identity_processor import IdentityProcessor, IdentityTransformationType

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockFramework:
    """Mock framework for testing"""
    def __init__(self):
        self.config = MockConfig()


class MockConfig:
    """Mock config for testing"""
    MODELS_DIR = Path("models")


def test_identity_processor():
    """Test the Identity Processor plugin"""
    logger.info("🧪 Testing Identity Processor Plugin")
    
    # Initialize the identity processor
    framework = MockFramework()
    identity_processor = IdentityProcessor(framework)
    
    # Test content from Relic story about Shay
    test_content = """
    Shay sat on a log at the edge of the cliff's edge overlooking the dense forest below her. 
    The wind gently blowing her brilliant ruby red hair as it glitters in the moon light. 
    Shay is a young woman with ruby red hair who stands at the center of the village. 
    Shay cautiously approaches the shopkeeper and gently says "Hello sir." 
    Shay hands the shopkeeper her old beat-up leather sheath and says "I was looking to get a new one. I don't have much to offer."
    Shay empties her pockets only to have a few gold pieces in her hand.
    """
    
    logger.info("📖 Original content:")
    logger.info(test_content)
    
    # Test identity transformation
    logger.info("\n🔄 Testing identity transformation...")
    
    # Test full identity transformation
    transformed_content = identity_processor.transform_content_to_identity(
        "Shay", 
        test_content, 
        IdentityTransformationType.FULL_IDENTITY
    )
    
    logger.info("✅ Transformed content (FULL_IDENTITY):")
    logger.info(transformed_content)
    
    # Test partial identity transformation
    partial_transformed = identity_processor.transform_content_to_identity(
        "Shay", 
        test_content, 
        IdentityTransformationType.PARTIAL_IDENTITY
    )
    
    logger.info("\n✅ Transformed content (PARTIAL_IDENTITY):")
    logger.info(partial_transformed)
    
    # Test identity profile extraction
    logger.info("\n🔍 Testing identity profile extraction...")
    
    identity_profile = identity_processor.extract_identity_from_content("Shay", transformed_content)
    
    logger.info("✅ Extracted identity profile:")
    logger.info(f"Name: {identity_profile.name}")
    logger.info(f"Core Identity: {identity_profile.core_identity}")
    logger.info(f"Identity Traits: {identity_profile.identity_traits}")
    logger.info(f"Voice Identity: {identity_profile.voice_identity}")
    logger.info(f"Background Identity: {identity_profile.background_identity}")
    logger.info(f"Identity Phrases: {identity_profile.identity_phrases}")
    
    # Test content processing as identity
    logger.info("\n🔄 Testing content processing as identity...")
    
    result = identity_processor.process_content_as_identity(
        "Shay", 
        test_content, 
        IdentityTransformationType.FULL_IDENTITY
    )
    
    logger.info("✅ Processing result:")
    logger.info(f"Success: {result['success']}")
    logger.info(f"Message: {result['message']}")
    logger.info(f"Transformation Type: {result['transformation_type']}")
    
    # Test identity statistics
    logger.info("\n📊 Testing identity statistics...")
    
    stats = identity_processor.get_identity_stats()
    logger.info("✅ Identity statistics:")
    for key, value in stats.items():
        logger.info(f"{key}: {value}")
    
    # Test active identities
    logger.info("\n🎭 Testing active identities...")
    
    active_identities = identity_processor.get_active_identities()
    logger.info(f"✅ Active identities: {active_identities}")
    
    # Test identity profile retrieval
    logger.info("\n👤 Testing identity profile retrieval...")
    
    profile = identity_processor.get_identity_profile("Shay")
    if profile:
        logger.info(f"✅ Retrieved profile for Shay: {profile.name}")
        logger.info(f"Core Identity: {profile.core_identity}")
    else:
        logger.error("❌ Failed to retrieve Shay's profile")
    
    # Test deactivation
    logger.info("\n🔄 Testing identity deactivation...")
    
    deactivate_result = identity_processor.deactivate_identity("Shay")
    logger.info(f"✅ Deactivation result: {deactivate_result}")
    
    # Verify deactivation
    active_after_deactivation = identity_processor.get_active_identities()
    logger.info(f"✅ Active identities after deactivation: {active_after_deactivation}")
    
    logger.info("\n🎉 Identity Processor test completed successfully!")


def test_with_real_book_content():
    """Test with real book content from Relic story"""
    logger.info("\n📚 Testing with real book content...")
    
    # Initialize the identity processor
    framework = MockFramework()
    identity_processor = IdentityProcessor(framework)
    
    # Read real book content
    book_path = Path("Book_Collection/Relic/Chapter_1.txt")
    if book_path.exists():
        with open(book_path, 'r', encoding='utf-8') as f:
            book_content = f.read()
        
        logger.info(f"📖 Loaded {len(book_content)} characters from Chapter 1")
        
        # Extract a sample section about Shay
        shay_sections = []
        lines = book_content.split('\n')
        for i, line in enumerate(lines):
            if 'Shay' in line:
                # Get context around Shay mentions
                start = max(0, i-2)
                end = min(len(lines), i+3)
                context = '\n'.join(lines[start:end])
                shay_sections.append(context)
        
        if shay_sections:
            sample_content = '\n'.join(shay_sections[:3])  # First 3 sections
            logger.info(f"📝 Sample content about Shay ({len(sample_content)} characters):")
            logger.info(sample_content[:500] + "..." if len(sample_content) > 500 else sample_content)
            
            # Test identity transformation
            logger.info("\n🔄 Testing identity transformation with real content...")
            
            transformed = identity_processor.transform_content_to_identity(
                "Shay", 
                sample_content, 
                IdentityTransformationType.FULL_IDENTITY
            )
            
            logger.info("✅ Transformed real content:")
            logger.info(transformed[:500] + "..." if len(transformed) > 500 else transformed)
            
            # Test identity profile extraction
            profile = identity_processor.extract_identity_from_content("Shay", transformed)
            
            logger.info("\n✅ Extracted identity profile from real content:")
            logger.info(f"Core Identity: {profile.core_identity}")
            logger.info(f"Identity Traits: {profile.identity_traits}")
            logger.info(f"Voice Identity: {profile.voice_identity}")
            logger.info(f"Identity Phrases: {profile.identity_phrases[:3]}...")  # First 3 phrases
            
        else:
            logger.warning("⚠️ No Shay content found in Chapter 1")
    else:
        logger.error("❌ Book file not found: {book_path}")


if __name__ == "__main__":
    logger.info("🚀 Starting Identity Processor Plugin Tests")
    
    try:
        # Test basic functionality
        test_identity_processor()
        
        # Test with real book content
        test_with_real_book_content()
        
        logger.info("✅ All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 