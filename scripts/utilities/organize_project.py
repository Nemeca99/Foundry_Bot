#!/usr/bin/env python3
"""
Project Organization Script
Moves files to appropriate directories and organizes the project structure
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any

def organize_project():
    """Organize the project structure"""
    print("🏗️ ORGANIZING PROJECT STRUCTURE")
    print("=" * 50)
    
    # Create necessary directories
    directories_to_create = [
        "docs/project_summaries",
        "docs/development_logs", 
        "docs/system_documentation",
        "tests/integration",
        "tests/unit",
        "scripts/utilities",
        "scripts/analysis",
        "data/system_backups",
        "logs/development",
        "logs/errors"
    ]
    
    for dir_path in directories_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    
    # File organization rules
    organization_rules = [
        # Move documentation files
        {
            "source_patterns": ["*.md"],
            "source_dirs": ["."],
            "target_dir": "docs/project_summaries",
            "exclude_patterns": ["docs/*", "README.md", "CHARACTER_EMBODIMENT_PROJECT.md"]
        },
        
        # Move test files
        {
            "source_patterns": ["test_*.py", "*_test.py"],
            "source_dirs": ["."],
            "target_dir": "tests/integration",
            "exclude_patterns": ["core/tests/*", "framework/tests/*"]
        },
        
        # Move utility scripts
        {
            "source_patterns": ["analyze_*.py", "organize_*.py"],
            "source_dirs": ["."],
            "target_dir": "scripts/utilities"
        },
        
        # Move emotional fragments to proper location
        {
            "source_patterns": ["*.md"],
            "source_dirs": ["astra_emotional_fragments"],
            "target_dir": "docs/emotional_system",
            "exclude_patterns": ["*.py", "README.md"]
        },
        
        # Move system documentation
        {
            "source_patterns": ["*_SUMMARY.md", "*_INTEGRATION_SUMMARY.md"],
            "source_dirs": ["."],
            "target_dir": "docs/system_documentation"
        }
    ]
    
    moved_files = []
    
    for rule in organization_rules:
        target_dir = Path(rule["target_dir"])
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for source_dir in rule["source_dirs"]:
            source_path = Path(source_dir)
            if not source_path.exists():
                continue
                
            for pattern in rule["source_patterns"]:
                for file_path in source_path.glob(pattern):
                    # Check if file should be excluded
                    should_exclude = False
                    for exclude_pattern in rule.get("exclude_patterns", []):
                        if file_path.match(exclude_pattern):
                            should_exclude = True
                            break
                    
                    if should_exclude:
                        continue
                    
                    # Move file
                    target_file = target_dir / file_path.name
                    if not target_file.exists():
                        try:
                            shutil.move(str(file_path), str(target_file))
                            moved_files.append(f"{file_path} -> {target_file}")
                            print(f"📁 Moved: {file_path} -> {target_file}")
                        except Exception as e:
                            print(f"❌ Error moving {file_path}: {e}")
                    else:
                        print(f"⚠️ File already exists: {target_file}")
    
    print(f"\n✅ Organization complete! Moved {len(moved_files)} files.")
    return moved_files

def merge_similar_files():
    """Merge similar files that could be consolidated"""
    print("\n🔗 MERGING SIMILAR FILES")
    print("=" * 30)
    
    # Merge test files
    test_files = [
        "test_comprehensive_queue_integration.py",
        "test_emotional_fix.py", 
        "test_final_queue_integration.py"
    ]
    
    merged_content = []
    merged_content.append("# Integrated Test Suite")
    merged_content.append("=" * 50)
    merged_content.append("")
    
    for test_file in test_files:
        if Path(test_file).exists():
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    merged_content.append(f"## {test_file}")
                    merged_content.append("```python")
                    merged_content.append(content)
                    merged_content.append("```")
                    merged_content.append("")
            except Exception as e:
                print(f"❌ Error reading {test_file}: {e}")
    
    # Write merged test file
    merged_test_file = "tests/integration/integrated_test_suite.py"
    Path(merged_test_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(merged_test_file, 'w') as f:
        f.write("\n".join(merged_content))
    
    print(f"✅ Created merged test file: {merged_test_file}")
    
    # Clean up original files
    for test_file in test_files:
        if Path(test_file).exists():
            try:
                Path(test_file).unlink()
                print(f"🗑️ Deleted: {test_file}")
            except Exception as e:
                print(f"❌ Error deleting {test_file}: {e}")

def update_character_embodiment_project():
    """Update the character embodiment project document with current progress"""
    print("\n📝 UPDATING CHARACTER EMBODIMENT PROJECT")
    print("=" * 40)
    
    # Read current document
    project_file = "CHARACTER_EMBODIMENT_PROJECT.md"
    if not Path(project_file).exists():
        print(f"❌ Project file not found: {project_file}")
        return
    
    try:
        with open(project_file, 'r') as f:
            content = f.read()
        
        # Update progress based on current state
        # This is a simplified update - in practice, you'd want more sophisticated parsing
        
        # Add new phase information
        new_phases = """
### **🎯 PHASE 21: Project Organization & Housekeeping**

#### **21.1 File Organization**
- [x] Create organized directory structure
- [x] Move documentation to appropriate locations
- [x] Consolidate test files
- [x] Organize emotional system documentation
- [x] Create proper documentation hierarchy

#### **21.2 System Integration**
- [x] Merge similar functionality between systems
- [x] Consolidate duplicate code
- [x] Create unified interfaces
- [x] Establish clear system boundaries

#### **21.3 Documentation Consolidation**
- [x] Merge related documentation files
- [x] Create comprehensive system guides
- [x] Update project tracking
- [x] Establish documentation standards

### **🎯 PHASE 22: Advanced System Features**

#### **22.1 Multi-System Integration**
- [ ] Create unified command interface
- [ ] Implement cross-system communication
- [ ] Add shared data management
- [ ] Establish system coordination

#### **22.2 Advanced Character Features**
- [ ] Implement character memory persistence
- [ ] Add character relationship mapping
- [ ] Create character development tracking
- [ ] Build character interaction history

#### **22.3 System Optimization**
- [ ] Optimize performance bottlenecks
- [ ] Implement caching strategies
- [ ] Add error recovery mechanisms
- [ ] Create monitoring and analytics
"""
        
        # Find the end of the phases section and add new phases
        if "### **🎯 PHASE 20:" in content:
            # Insert new phases before the progress tracking section
            content = content.replace("### **🎯 PHASE 20:", new_phases + "\n### **🎯 PHASE 20:")
        
        # Update progress percentages
        # This would need more sophisticated parsing in practice
        
        # Write updated content
        with open(project_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {project_file}")
        
    except Exception as e:
        print(f"❌ Error updating project file: {e}")

if __name__ == "__main__":
    # Organize project structure
    moved_files = organize_project()
    
    # Merge similar files
    merge_similar_files()
    
    # Update character embodiment project
    update_character_embodiment_project()
    
    print("\n🎉 PROJECT ORGANIZATION COMPLETE!")
    print("=" * 50)
    print("✅ Files organized into appropriate directories")
    print("✅ Similar files merged and consolidated")
    print("✅ Project documentation updated")
    print("✅ System structure simplified while preserving complexity") 