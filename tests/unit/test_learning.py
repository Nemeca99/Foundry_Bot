#!/usr/bin/env python3
"""
Test script for Learning Engine
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_learning_engine():
    """Test the learning engine functionality"""
    print("Testing Learning Engine...")
    print("=" * 40)

    # Initialize framework
    framework = get_framework()

    # Check if learning engine plugin is loaded
    if "learning_engine" not in framework.plugins:
        print("❌ Learning Engine plugin not found!")
        print("Available plugins:", list(framework.plugins.keys()))
        return False

    learning_engine = framework.plugins["learning_engine"]
    print("✅ Learning Engine plugin loaded successfully")

    # Test configuration
    print(f"\n🔧 Configuration:")
    print(f"   Chunk size: {learning_engine.chunk_size}")
    print(f"   Overlap size: {learning_engine.overlap_size}")
    print(f"   Max workers: {learning_engine.max_workers}")
    print(f"   Wikipedia path: {learning_engine.wikipedia_path}")
    print(f"   Book collection path: {learning_engine.book_collection_path}")
    print(f"   Output directory: {learning_engine.output_dir}")

    # Check paths
    print(f"\n📁 Path Status:")
    print(f"   Wikipedia exists: {learning_engine.wikipedia_path.exists()}")
    print(f"   Book collection exists: {learning_engine.book_collection_path.exists()}")
    print(f"   Output directory exists: {learning_engine.output_dir.exists()}")

    # Test stats
    print(f"\n📊 Current Statistics:")
    stats = learning_engine.get_learning_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Test with a small Wikipedia sample (if available)
    if learning_engine.wikipedia_path.exists():
        print(f"\n🔍 Testing Wikipedia processing...")
        wikipedia_files = list(learning_engine.wikipedia_path.rglob("*.txt"))
        if wikipedia_files:
            print(f"   Found {len(wikipedia_files)} Wikipedia files")
            # Test with just 1 file
            test_file = wikipedia_files[0]
            print(f"   Testing with: {test_file.name}")

            chunks = learning_engine._process_wikipedia_file(test_file)
            print(f"   Generated {len(chunks)} chunks from test file")

            if chunks:
                print(
                    f"   Sample chunk content (first 100 chars): {chunks[0].content[:100]}..."
                )
        else:
            print("   No Wikipedia text files found")

    # Test book collection processing
    if learning_engine.book_collection_path.exists():
        print(f"\n📚 Testing Book Collection processing...")
        book_files = list(learning_engine.book_collection_path.rglob("*.txt"))
        if book_files:
            print(f"   Found {len(book_files)} book files")
            # Test with just 1 file
            test_file = book_files[0]
            print(f"   Testing with: {test_file.name}")

            chunks = learning_engine._process_book_file(test_file)
            print(f"   Generated {len(chunks)} chunks from test file")

            if chunks:
                print(
                    f"   Sample chunk content (first 100 chars): {chunks[0].content[:100]}..."
                )
        else:
            print("   No book text files found")

    print(f"\n✅ Learning Engine test completed!")
    return True


if __name__ == "__main__":
    test_learning_engine()
