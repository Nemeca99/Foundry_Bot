#!/usr/bin/env python3
"""
Framework CLI Tool - Comprehensive Framework Management System
Provides file analysis, compression, merging, and cleanup capabilities
"""

import os
import sys
import json
import shutil
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
import difflib

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FrameworkCLI:
    """Comprehensive CLI tool for framework management"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.framework = get_framework()
        self.file_analysis = {}
        self.compression_stats = {}
        
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze the entire project structure and file organization"""
        logger.info("🔍 Analyzing project structure...")
        
        analysis = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "directory_structure": {},
            "duplicate_files": [],
            "large_files": [],
            "unused_files": [],
            "potential_merges": [],
            "compression_opportunities": []
        }
        
        # Walk through all directories
        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environments and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', '.venv']]
            
            rel_path = Path(root).relative_to(self.project_root)
            analysis["directory_structure"][str(rel_path)] = {
                "files": len(files),
                "subdirs": len(dirs),
                "file_list": files
            }
            analysis["total_directories"] += 1
            
            for file in files:
                file_path = Path(root) / file
                rel_file_path = file_path.relative_to(self.project_root)
                
                # Get file info
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
                    analysis["large_files"].append({
                        "path": str(rel_file_path),
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })
                
                # Check for potential duplicates
                file_hash = self._get_file_hash(file_path)
                if file_hash in self.file_analysis:
                    analysis["duplicate_files"].append({
                        "original": self.file_analysis[file_hash],
                        "duplicate": str(rel_file_path),
                        "hash": file_hash
                    })
                else:
                    self.file_analysis[file_hash] = str(rel_file_path)
        
        # Identify potential merges
        analysis["potential_merges"] = self._identify_potential_merges()
        
        # Identify compression opportunities
        analysis["compression_opportunities"] = self._identify_compression_opportunities()
        
        logger.info(f"✅ Analysis complete: {analysis['total_files']} files, {analysis['total_directories']} directories")
        return analysis
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _identify_potential_merges(self) -> List[Dict[str, Any]]:
        """Identify files that could potentially be merged"""
        potential_merges = []
        
        # Look for similar files in same directory
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in root or '.venv' in root:
                continue
                
            # Group files by similarity
            file_groups = {}
            for file in files:
                if file.endswith('.py'):
                    base_name = file.replace('.py', '')
                    if base_name not in file_groups:
                        file_groups[base_name] = []
                    file_groups[base_name].append(file)
            
            # Check for potential merges
            for base_name, file_list in file_groups.items():
                if len(file_list) > 1:
                    potential_merges.append({
                        "directory": str(Path(root).relative_to(self.project_root)),
                        "base_name": base_name,
                        "files": file_list,
                        "merge_type": "similar_names"
                    })
        
        return potential_merges
    
    def _identify_compression_opportunities(self) -> List[Dict[str, Any]]:
        """Identify files that could be compressed"""
        compression_opportunities = []
        
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in root or '.venv' in root:
                continue
                
            for file in files:
                file_path = Path(root) / file
                file_size = file_path.stat().st_size
                
                # Check for large text files that could be compressed
                if file_size > 100 * 1024 and file.suffix in ['.txt', '.md', '.json', '.log']:
                    compression_opportunities.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "compression_type": "text_compression"
                    })
                
                # Check for large image/video files
                elif file_size > 5 * 1024 * 1024 and file.suffix in ['.png', '.jpg', '.jpeg', '.mp4', '.avi']:
                    compression_opportunities.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "compression_type": "media_compression"
                    })
        
        return compression_opportunities
    
    def show_file_analysis(self, analysis: Dict[str, Any]):
        """Display file analysis results"""
        print("\n" + "="*80)
        print("📊 FRAMEWORK FILE ANALYSIS")
        print("="*80)
        
        print(f"\n📁 Project Structure:")
        print(f"   Total Files: {analysis['total_files']:,}")
        print(f"   Total Directories: {analysis['total_directories']:,}")
        
        print(f"\n📄 File Types:")
        for ext, info in sorted(analysis['file_types'].items(), key=lambda x: x[1]['count'], reverse=True):
            size_mb = round(info['total_size'] / (1024 * 1024), 2)
            print(f"   {ext or 'no extension'}: {info['count']:,} files ({size_mb} MB)")
        
        if analysis['large_files']:
            print(f"\n📦 Large Files (>1MB):")
            for file_info in sorted(analysis['large_files'], key=lambda x: x['size'], reverse=True)[:10]:
                print(f"   {file_info['path']}: {file_info['size_mb']} MB")
        
        if analysis['duplicate_files']:
            print(f"\n🔄 Duplicate Files:")
            for dup in analysis['duplicate_files'][:5]:
                print(f"   {dup['original']} <-> {dup['duplicate']}")
        
        if analysis['potential_merges']:
            print(f"\n🔗 Potential Merges:")
            for merge in analysis['potential_merges'][:5]:
                print(f"   {merge['directory']}/{merge['base_name']}: {merge['files']}")
        
        if analysis['compression_opportunities']:
            print(f"\n🗜️ Compression Opportunities:")
            for comp in sorted(analysis['compression_opportunities'], key=lambda x: x['size'], reverse=True)[:5]:
                print(f"   {comp['file']}: {comp['size_mb']} MB ({comp['compression_type']})")
    
    def compress_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Compress files based on analysis"""
        logger.info("🗜️ Starting file compression...")
        
        compression_results = {
            "compressed_files": [],
            "saved_space": 0,
            "compression_ratio": 0.0
        }
        
        # Create compression directory
        compression_dir = self.project_root / "compressed"
        compression_dir.mkdir(exist_ok=True)
        
        for comp_opp in analysis['compression_opportunities']:
            file_path = self.project_root / comp_opp['file']
            
            if file_path.exists():
                try:
                    # Create compressed version
                    compressed_path = compression_dir / f"{file_path.stem}_compressed{file_path.suffix}.gz"
                    
                    import gzip
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Calculate savings
                    original_size = file_path.stat().st_size
                    compressed_size = compressed_path.stat().st_size
                    saved_space = original_size - compressed_size
                    
                    compression_results["compressed_files"].append({
                        "original": str(file_path.relative_to(self.project_root)),
                        "compressed": str(compressed_path.relative_to(self.project_root)),
                        "original_size": original_size,
                        "compressed_size": compressed_size,
                        "saved_space": saved_space,
                        "compression_ratio": round((1 - compressed_size / original_size) * 100, 2)
                    })
                    
                    compression_results["saved_space"] += saved_space
                    
                except Exception as e:
                    logger.error(f"Failed to compress {file_path}: {e}")
        
        if compression_results["compressed_files"]:
            total_original = sum(f["original_size"] for f in compression_results["compressed_files"])
            total_compressed = sum(f["compressed_size"] for f in compression_results["compressed_files"])
            compression_results["compression_ratio"] = round((1 - total_compressed / total_original) * 100, 2)
        
        logger.info(f"✅ Compression complete: {len(compression_results['compressed_files'])} files compressed")
        return compression_results
    
    def merge_similar_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Merge similar files based on analysis"""
        logger.info("🔗 Starting file merging...")
        
        merge_results = {
            "merged_files": [],
            "created_files": [],
            "saved_files": 0
        }
        
        for merge_opp in analysis['potential_merges']:
            if merge_opp['merge_type'] == 'similar_names':
                directory = self.project_root / merge_opp['directory']
                base_name = merge_opp['base_name']
                files = merge_opp['files']
                
                if len(files) > 1:
                    try:
                        # Create merged file
                        merged_content = []
                        merged_content.append(f"# Merged from: {', '.join(files)}")
                        merged_content.append(f"# Merged on: {datetime.now().isoformat()}")
                        merged_content.append("")
                        
                        for file in files:
                            file_path = directory / file
                            if file_path.exists():
                                merged_content.append(f"# === {file} ===")
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    merged_content.append(f.read())
                                merged_content.append("")
                        
                        # Write merged file
                        merged_file = directory / f"{base_name}_merged.py"
                        with open(merged_file, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(merged_content))
                        
                        merge_results["merged_files"].append({
                            "directory": merge_opp['directory'],
                            "base_name": base_name,
                            "original_files": files,
                            "merged_file": str(merged_file.relative_to(self.project_root))
                        })
                        
                        merge_results["created_files"].append(str(merged_file.relative_to(self.project_root)))
                        merge_results["saved_files"] += len(files) - 1
                        
                    except Exception as e:
                        logger.error(f"Failed to merge files in {merge_opp['directory']}: {e}")
        
        logger.info(f"✅ Merging complete: {len(merge_results['merged_files'])} groups merged")
        return merge_results
    
    def cleanup_unused_files(self) -> Dict[str, Any]:
        """Clean up unused files and directories"""
        logger.info("🧹 Starting cleanup...")
        
        cleanup_results = {
            "removed_files": [],
            "removed_directories": [],
            "saved_space": 0
        }
        
        # Remove __pycache__ directories
        for root, dirs, files in os.walk(self.project_root):
            if '__pycache__' in dirs:
                cache_dir = Path(root) / '__pycache__'
                try:
                    # Calculate size before removal
                    total_size = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
                    
                    shutil.rmtree(cache_dir)
                    cleanup_results["removed_directories"].append(str(cache_dir.relative_to(self.project_root)))
                    cleanup_results["saved_space"] += total_size
                    
                except Exception as e:
                    logger.error(f"Failed to remove {cache_dir}: {e}")
        
        # Remove .pyc files
        for pyc_file in self.project_root.rglob('*.pyc'):
            try:
                size = pyc_file.stat().st_size
                pyc_file.unlink()
                cleanup_results["removed_files"].append(str(pyc_file.relative_to(self.project_root)))
                cleanup_results["saved_space"] += size
            except Exception as e:
                logger.error(f"Failed to remove {pyc_file}: {e}")
        
        logger.info(f"✅ Cleanup complete: {len(cleanup_results['removed_files'])} files, {len(cleanup_results['removed_directories'])} directories removed")
        return cleanup_results
    
    def show_compression_results(self, results: Dict[str, Any]):
        """Display compression results"""
        print("\n" + "="*80)
        print("🗜️ COMPRESSION RESULTS")
        print("="*80)
        
        if results["compressed_files"]:
            print(f"\n📦 Compressed Files: {len(results['compressed_files'])}")
            for file_info in results["compressed_files"]:
                print(f"   {file_info['original']} -> {file_info['compressed']}")
                print(f"     Size: {file_info['original_size']:,} -> {file_info['compressed_size']:,} bytes")
                print(f"     Saved: {file_info['saved_space']:,} bytes ({file_info['compression_ratio']}%)")
            
            print(f"\n💾 Total Space Saved: {results['saved_space']:,} bytes ({results['compression_ratio']}%)")
        else:
            print("\n📦 No files were compressed")
    
    def show_merge_results(self, results: Dict[str, Any]):
        """Display merge results"""
        print("\n" + "="*80)
        print("🔗 MERGE RESULTS")
        print("="*80)
        
        if results["merged_files"]:
            print(f"\n🔗 Merged File Groups: {len(results['merged_files'])}")
            for merge_info in results["merged_files"]:
                print(f"   Directory: {merge_info['directory']}")
                print(f"   Base Name: {merge_info['base_name']}")
                print(f"   Original Files: {merge_info['original_files']}")
                print(f"   Merged File: {merge_info['merged_file']}")
                print()
            
            print(f"📁 Created Files: {len(results['created_files'])}")
            print(f"💾 Saved Files: {results['saved_files']}")
        else:
            print("\n🔗 No files were merged")
    
    def show_cleanup_results(self, results: Dict[str, Any]):
        """Display cleanup results"""
        print("\n" + "="*80)
        print("🧹 CLEANUP RESULTS")
        print("="*80)
        
        if results["removed_files"] or results["removed_directories"]:
            print(f"\n🗑️ Removed Files: {len(results['removed_files'])}")
            for file in results["removed_files"][:10]:  # Show first 10
                print(f"   {file}")
            
            print(f"\n📁 Removed Directories: {len(results['removed_directories'])}")
            for directory in results["removed_directories"]:
                print(f"   {directory}")
            
            print(f"\n💾 Space Saved: {results['saved_space']:,} bytes")
        else:
            print("\n🧹 No cleanup performed")
    
    def interactive_mode(self):
        """Run interactive CLI mode"""
        print("\n" + "="*80)
        print("🛠️ FRAMEWORK CLI - INTERACTIVE MODE")
        print("="*80)
        
        while True:
            print("\n📋 Available Commands:")
            print("  1. Analyze project structure")
            print("  2. Show file analysis")
            print("  3. Compress files")
            print("  4. Merge similar files")
            print("  5. Cleanup unused files")
            print("  6. Show all results")
            print("  7. Export analysis to JSON")
            print("  0. Exit")
            
            choice = input("\n🔧 Enter your choice (0-7): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.analysis = self.analyze_project_structure()
                print("✅ Analysis complete!")
            elif choice == "2":
                if hasattr(self, 'analysis'):
                    self.show_file_analysis(self.analysis)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "3":
                if hasattr(self, 'analysis'):
                    self.compression_results = self.compress_files(self.analysis)
                    self.show_compression_results(self.compression_results)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "4":
                if hasattr(self, 'analysis'):
                    self.merge_results = self.merge_similar_files(self.analysis)
                    self.show_merge_results(self.merge_results)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "5":
                self.cleanup_results = self.cleanup_unused_files()
                self.show_cleanup_results(self.cleanup_results)
            elif choice == "6":
                if hasattr(self, 'analysis'):
                    self.show_file_analysis(self.analysis)
                if hasattr(self, 'compression_results'):
                    self.show_compression_results(self.compression_results)
                if hasattr(self, 'merge_results'):
                    self.show_merge_results(self.merge_results)
                if hasattr(self, 'cleanup_results'):
                    self.show_cleanup_results(self.cleanup_results)
            elif choice == "7":
                if hasattr(self, 'analysis'):
                    self.export_analysis()
                else:
                    print("❌ Please run analysis first (option 1)")
            else:
                print("❌ Invalid choice. Please try again.")
    
    def export_analysis(self):
        """Export analysis results to JSON"""
        if hasattr(self, 'analysis'):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "analysis": self.analysis
            }
            
            if hasattr(self, 'compression_results'):
                export_data["compression_results"] = self.compression_results
            
            if hasattr(self, 'merge_results'):
                export_data["merge_results"] = self.merge_results
            
            if hasattr(self, 'cleanup_results'):
                export_data["cleanup_results"] = self.cleanup_results
            
            export_file = self.project_root / "framework_analysis.json"
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Analysis exported to: {export_file}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Framework CLI Management Tool")
    parser.add_argument("--analyze", action="store_true", help="Analyze project structure")
    parser.add_argument("--compress", action="store_true", help="Compress files")
    parser.add_argument("--merge", action="store_true", help="Merge similar files")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup unused files")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--export", action="store_true", help="Export analysis to JSON")
    
    args = parser.parse_args()
    
    cli = FrameworkCLI()
    
    if args.interactive:
        cli.interactive_mode()
    else:
        # Run analysis first
        analysis = cli.analyze_project_structure()
        cli.show_file_analysis(analysis)
        
        if args.compress:
            compression_results = cli.compress_files(analysis)
            cli.show_compression_results(compression_results)
        
        if args.merge:
            merge_results = cli.merge_similar_files(analysis)
            cli.show_merge_results(merge_results)
        
        if args.cleanup:
            cleanup_results = cli.cleanup_unused_files()
            cli.show_cleanup_results(cleanup_results)
        
        if args.export:
            cli.analysis = analysis
            cli.export_analysis()


if __name__ == "__main__":
    main() 