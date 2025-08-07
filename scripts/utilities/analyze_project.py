#!/usr/bin/env python3
"""
Simple Project Analysis Script
Analyzes the project structure and identifies files that need organization
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def analyze_project_structure() -> Dict[str, Any]:
    """Analyze the project structure"""
    project_root = Path(".")

    analysis = {
        "total_files": 0,
        "total_directories": 0,
        "file_types": {},
        "directory_structure": {},
        "large_files": [],
        "framework_plugins": [],
        "discord_bots": [],
        "potential_merges": [],
        "unorganized_files": [],
    }

    # Walk through all directories
    for root, dirs, files in os.walk(project_root):
        # Skip virtual environments and cache
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["__pycache__", ".venv", ".git"]
        ]

        rel_path = Path(root).relative_to(project_root)
        analysis["directory_structure"][str(rel_path)] = {
            "files": len(files),
            "subdirs": len(dirs),
            "file_list": files,
        }
        analysis["total_directories"] += 1

        for file in files:
            file_path = Path(root) / file
            rel_file_path = file_path.relative_to(project_root)

            # Get file info
            try:
                file_size = file_path.stat().st_size
                file_ext = file_path.suffix.lower()

                analysis["total_files"] += 1

                # Track file types
                if file_ext not in analysis["file_types"]:
                    analysis["file_types"][file_ext] = {"count": 0, "total_size": 0}
                analysis["file_types"][file_ext]["count"] += 1
                analysis["file_types"][file_ext]["total_size"] += file_size

                # Identify large files (>1MB)
                if file_size > 1024 * 1024:
                    analysis["large_files"].append(
                        {
                            "path": str(rel_file_path),
                            "size": file_size,
                            "size_mb": round(file_size / (1024 * 1024), 2),
                        }
                    )

                # Track framework plugins
                if "framework/plugins" in str(rel_file_path) and file.endswith(".py"):
                    analysis["framework_plugins"].append(str(rel_file_path))

                # Track Discord bots
                if "discord" in str(rel_file_path) and file.endswith("_bot.py"):
                    analysis["discord_bots"].append(str(rel_file_path))

                # Identify unorganized files
                if file.endswith(".md") and "docs" not in str(rel_file_path):
                    analysis["unorganized_files"].append(str(rel_file_path))
                elif (
                    file.endswith(".py")
                    and "framework" not in str(rel_file_path)
                    and "discord" not in str(rel_file_path)
                    and "scripts" not in str(rel_file_path)
                ):
                    analysis["unorganized_files"].append(str(rel_file_path))

            except (OSError, FileNotFoundError):
                continue

    # Identify potential merges
    analysis["potential_merges"] = identify_potential_merges()

    return analysis


def identify_potential_merges() -> List[Dict[str, Any]]:
    """Identify files that could be merged"""
    potential_merges = []

    # Look for similar files that could be merged
    merge_patterns = [
        {
            "pattern": ["*_bot.py", "*bot*.py"],
            "description": "Discord bot files that could be unified",
        },
        {
            "pattern": ["*_test.py", "test_*.py"],
            "description": "Test files that could be organized",
        },
        {
            "pattern": ["*.md", "*.txt"],
            "description": "Documentation files that could be consolidated",
        },
    ]

    return potential_merges


def show_analysis(analysis: Dict[str, Any]):
    """Display the analysis results"""
    print("PROJECT STRUCTURE ANALYSIS")
    print("=" * 50)

    print(f"\nOVERVIEW:")
    print(f"  Total Files: {analysis['total_files']}")
    print(f"  Total Directories: {analysis['total_directories']}")

    print(f"\nDIRECTORY STRUCTURE:")
    for dir_path, info in analysis["directory_structure"].items():
        if info["files"] > 0:
            print(f"  {dir_path}: {info['files']} files, {info['subdirs']} subdirs")

    print(f"\nFRAMEWORK PLUGINS ({len(analysis['framework_plugins'])}):")
    for plugin in analysis["framework_plugins"]:
        print(f"  {plugin}")

    print(f"\nDISCORD BOTS ({len(analysis['discord_bots'])}):")
    for bot in analysis["discord_bots"]:
        print(f"  {bot}")

    print(f"\nLARGE FILES ({len(analysis['large_files'])}):")
    for file in analysis["large_files"]:
        print(f"  {file['path']} ({file['size_mb']}MB)")

    print(f"\nUNORGANIZED FILES ({len(analysis['unorganized_files'])}):")
    for file in analysis["unorganized_files"]:
        print(f"  {file}")

    print(f"\nFILE TYPES:")
    for ext, info in analysis["file_types"].items():
        if info["count"] > 0:
            print(f"  {ext}: {info['count']} files ({info['total_size']} bytes)")


if __name__ == "__main__":
    # Set console encoding for Windows
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    
    analysis = analyze_project_structure()
    show_analysis(analysis)

    # Save analysis to file
    with open("project_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"\nAnalysis saved to project_analysis.json") 