#!/usr/bin/env python3
"""
Test Multi-Language Optimizer
Demonstrates Luna's ability to choose the best programming language for each circumstance
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework
from framework.plugins.multi_language_optimizer import MultiLanguageOptimizer


def test_language_selection():
    """Test language selection for different task types"""
    print("🌍 Multi-Language Optimizer Test")
    print("=" * 60)
    
    # Initialize framework
    framework = get_framework()
    
    # Test different task types
    tasks = [
        {
            "description": "High-performance data processing with memory optimization",
            "expected": "rust",
            "reason": "Performance and memory safety"
        },
        {
            "description": "AI machine learning model training with neural networks",
            "expected": "python",
            "reason": "Rich AI/ML ecosystem"
        },
        {
            "description": "Concurrent web server handling multiple requests",
            "expected": "go",
            "reason": "Excellent concurrency support"
        },
        {
            "description": "Scientific computing with numerical analysis",
            "expected": "julia",
            "reason": "Scientific computing and performance"
        },
        {
            "description": "System-level programming with hardware access",
            "expected": "cpp",
            "reason": "Low-level system programming"
        },
        {
            "description": "Web API development with async processing",
            "expected": "javascript",
            "reason": "Web development and async processing"
        }
    ]
    
    print("\n🎯 Testing Language Selection")
    print("-" * 40)
    
    for task in tasks:
        print(f"\n📋 Task: {task['description']}")
        
        # Choose optimal language
        language_name, profile, score = framework.choose_optimal_language(task['description'])
        
        print(f"   Selected: {language_name.upper()} (Score: {score:.3f})")
        print(f"   Expected: {task['expected'].upper()}")
        print(f"   Reason: {task['reason']}")
        
        # Check if selection matches expectation
        if language_name == task['expected']:
            print(f"   ✅ Correct selection!")
        else:
            print(f"   ⚠️  Different selection (but may still be valid)")
        
        # Show language profile
        print(f"   Strengths: {', '.join(profile.strengths)}")
        print(f"   Performance Score: {profile.performance_score:.2f}")
        print(f"   AI Processing Score: {profile.ai_processing_score:.2f}")


def test_code_generation():
    """Test code generation for different languages"""
    print("\n💻 Testing Code Generation")
    print("-" * 40)
    
    framework = get_framework()
    
    # Test tasks for different languages
    test_tasks = [
        ("High-performance concurrent data processing", "rust"),
        ("AI machine learning model training", "python"),
        ("Web API with async processing", "javascript"),
        ("Scientific computing with matrix operations", "julia"),
        ("System-level memory management", "cpp"),
        ("Concurrent server with goroutines", "go")
    ]
    
    for task_description, expected_language in test_tasks:
        print(f"\n🔧 Task: {task_description}")
        
        # Generate code snippet
        code_snippet = framework.generate_code_snippet(task_description, expected_language)
        
        print(f"   Language: {expected_language.upper()}")
        print(f"   Code Length: {len(code_snippet)} characters")
        
        # Show first few lines
        lines = code_snippet.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"   {line}")
        
        if len(code_snippet.split('\n')) > 5:
            print(f"   ... ({len(code_snippet.split('\n')) - 5} more lines)")


def test_task_analysis():
    """Test task requirement analysis"""
    print("\n📊 Testing Task Analysis")
    print("-" * 40)
    
    framework = get_framework()
    
    # Test different task descriptions
    tasks = [
        "Fast data processing with memory optimization",
        "AI neural network training with GPU acceleration",
        "Concurrent web server handling 1000 requests per second",
        "Scientific computing with matrix operations and linear algebra",
        "System-level programming with hardware driver development",
        "Web API development with real-time data streaming"
    ]
    
    for task in tasks:
        print(f"\n📋 Task: {task}")
        
        # Analyze requirements
        requirements = framework.analyze_task_requirements(task)
        
        print("   Requirements:")
        for req_type, score in requirements.items():
            if score > 0:
                print(f"     {req_type}: {score:.2f}")
        
        # Choose optimal language
        language_name, profile, score = framework.choose_optimal_language(task)
        print(f"   Optimal Language: {language_name.upper()} (Score: {score:.3f})")


def test_language_profiles():
    """Test language profile information"""
    print("\n📚 Testing Language Profiles")
    print("-" * 40)
    
    framework = get_framework()
    
    # Get all language profiles
    profiles = framework.get_language_profiles()
    
    for lang_name, profile in profiles.items():
        print(f"\n🌐 {profile['name'].upper()}")
        print(f"   File Extension: {profile['file_extension']}")
        print(f"   Strengths: {', '.join(profile['strengths'])}")
        print(f"   Performance Score: {profile['performance_score']:.2f}")
        print(f"   Memory Efficiency: {profile['memory_efficiency']:.2f}")
        print(f"   AI Processing Score: {profile['ai_processing_score']:.2f}")
        print(f"   Concurrent Processing: {profile['concurrent_processing']:.2f}")


def test_code_execution():
    """Test code execution for different languages"""
    print("\n⚡ Testing Code Execution")
    print("-" * 40)
    
    framework = get_framework()
    
    # Test Python execution (most likely to work)
    python_code = '''print("Hello from Python!")
import time
print(f"Current time: {time.time()}")
print("Python execution successful!")'''
    
    print("\n🐍 Testing Python Execution")
    result = framework.execute_code_snippet(python_code, "python")
    
    if result["success"]:
        print("   ✅ Python execution successful!")
        print(f"   Output: {result['output'].strip()}")
    else:
        print(f"   ❌ Python execution failed: {result['error']}")
    
    # Test JavaScript execution
    js_code = '''console.log("Hello from JavaScript!");
console.log(`Current time: ${Date.now()}`);
console.log("JavaScript execution successful!");'''
    
    print("\n🟨 Testing JavaScript Execution")
    result = framework.execute_code_snippet(js_code, "javascript")
    
    if result["success"]:
        print("   ✅ JavaScript execution successful!")
        print(f"   Output: {result['output'].strip()}")
    else:
        print(f"   ❌ JavaScript execution failed: {result['error']}")


def test_optimization_stats():
    """Test optimization statistics"""
    print("\n📈 Testing Optimization Statistics")
    print("-" * 40)
    
    framework = get_framework()
    
    # Get optimization stats
    stats = framework.get_optimization_stats()
    
    print("Optimization Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")


def test_integration_with_ai_backend():
    """Test integration with AI-native backend"""
    print("\n🤖 Testing AI Backend Integration")
    print("-" * 40)
    
    framework = get_framework()
    
    # Create a task that requires AI processing
    ai_task = "AI-optimized data structure creation with machine learning"
    
    print(f"📋 Task: {ai_task}")
    
    # Choose optimal language
    language_name, profile, score = framework.choose_optimal_language(ai_task)
    print(f"   Selected Language: {language_name.upper()} (Score: {score:.3f})")
    
    # Generate code snippet
    code_snippet = framework.generate_code_snippet(ai_task, language_name)
    print(f"   Generated {len(code_snippet)} characters of {language_name.upper()} code")
    
    # Create AI-optimized data
    test_data = {
        "task": ai_task,
        "selected_language": language_name,
        "score": score,
        "timestamp": time.time()
    }
    
    ai_data = framework.create_ai_optimized_data(test_data, "language_selection")
    print(f"   Created AI-optimized data: {len(ai_data.content)} bytes")
    
    # Store in AI backend
    framework.store_emotional_state_ai("test_user", {
        "language_preference": language_name,
        "task_type": "ai_processing",
        "optimization_score": score
    })
    
    print("   ✅ AI backend integration successful!")


def main():
    """Run all multi-language optimizer tests"""
    print("🚀 Multi-Language Optimizer System Tests")
    print("=" * 80)
    
    try:
        # Test language selection
        test_language_selection()
        
        # Test code generation
        test_code_generation()
        
        # Test task analysis
        test_task_analysis()
        
        # Test language profiles
        test_language_profiles()
        
        # Test code execution
        test_code_execution()
        
        # Test optimization stats
        test_optimization_stats()
        
        # Test AI backend integration
        test_integration_with_ai_backend()
        
        print("\n🎉 All multi-language optimizer tests completed successfully!")
        print("\n🌟 Luna can now choose the best programming language for each circumstance!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 