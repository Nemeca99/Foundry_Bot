#!/usr/bin/env python3
"""
Framework CLI Tool - Simple Version
Provides file analysis, compression, merging, and cleanup capabilities
"""

import os
import sys
import json
import shutil
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
import gzip
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SimpleFrameworkCLI:
    """Simple CLI tool for framework management without full framework dependency"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.file_analysis = {}
        self.backup_dir = Path("D:/framework_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.current_backup_id = None

    def create_backup(self, operation_name: str = "operation") -> str:
        """Create a backup of the entire project before any file operations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"backup_{operation_name}_{timestamp}"
        backup_path = self.backup_dir / backup_id

        logger.info(f"🔄 Creating backup: {backup_path}")

        try:
            # Create backup directory
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy all project files to backup
            for item in self.project_root.rglob("*"):
                if item.is_file():
                    # Calculate relative path
                    rel_path = item.relative_to(self.project_root)
                    backup_file = backup_path / rel_path

                    # Create parent directories if needed
                    backup_file.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(item, backup_file)

            self.current_backup_id = backup_id
            logger.info(f"✅ Backup created successfully: {backup_path}")
            return str(backup_path)

        except Exception as e:
            logger.error(f"❌ Failed to create backup: {e}")
            return None

    def restore_backup(self, backup_id: str) -> bool:
        """Restore from a specific backup"""
        backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            logger.error(f"❌ Backup not found: {backup_path}")
            return False

        logger.info(f"🔄 Restoring from backup: {backup_path}")

        try:
            # Remove current project files (except backup and temp files)
            for item in self.project_root.rglob("*"):
                if item.is_file() and not any(
                    x in str(item) for x in ["backup", "temp", ".git"]
                ):
                    item.unlink()
                elif item.is_dir() and not any(
                    x in str(item) for x in ["backup", "temp", ".git"]
                ):
                    if not any(item.iterdir()):
                        item.rmdir()

            # Restore from backup
            for backup_file in backup_path.rglob("*"):
                if backup_file.is_file():
                    rel_path = backup_file.relative_to(backup_path)
                    restore_path = self.project_root / rel_path

                    # Create parent directories if needed
                    restore_path.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(backup_file, restore_path)

            logger.info(f"✅ Restore completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to restore backup: {e}")
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        backups = []

        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("backup_"):
                # Calculate backup size
                total_size = sum(
                    f.stat().st_size for f in backup_dir.rglob("*") if f.is_file()
                )

                # Get creation time
                creation_time = datetime.fromtimestamp(backup_dir.stat().st_ctime)

                backups.append(
                    {
                        "id": backup_dir.name,
                        "path": str(backup_dir),
                        "size": total_size,
                        "size_mb": round(total_size / (1024 * 1024), 2),
                        "created": creation_time.isoformat(),
                        "created_readable": creation_time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        return sorted(backups, key=lambda x: x["created"], reverse=True)

    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """Clean up old backups, keeping only the most recent ones"""
        backups = self.list_backups()

        if len(backups) <= keep_count:
            logger.info(
                f"✅ No cleanup needed. {len(backups)} backups (keeping {keep_count})"
            )
            return 0

        removed_count = 0
        for backup in backups[keep_count:]:
            backup_path = Path(backup["path"])
            try:
                shutil.rmtree(backup_path)
                logger.info(f"🗑️ Removed old backup: {backup['id']}")
                removed_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to remove backup {backup['id']}: {e}")

        logger.info(f"✅ Cleanup complete: {removed_count} old backups removed")
        return removed_count

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
            "compression_opportunities": [],
        }

        # Walk through all directories
        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environments and cache
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["__pycache__", ".venv"]
            ]

            rel_path = Path(root).relative_to(self.project_root)
            analysis["directory_structure"][str(rel_path)] = {
                "files": len(files),
                "subdirs": len(dirs),
                "file_list": files,
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
                    analysis["large_files"].append(
                        {
                            "path": str(rel_file_path),
                            "size": file_size,
                            "size_mb": round(file_size / (1024 * 1024), 2),
                        }
                    )

                # Check for potential duplicates
                file_hash = self._get_file_hash(file_path)
                if file_hash in self.file_analysis:
                    analysis["duplicate_files"].append(
                        {
                            "original": self.file_analysis[file_hash],
                            "duplicate": str(rel_file_path),
                            "hash": file_hash,
                        }
                    )
                else:
                    self.file_analysis[file_hash] = str(rel_file_path)

        # Identify potential merges
        analysis["potential_merges"] = self._identify_potential_merges()

        # Identify compression opportunities
        analysis["compression_opportunities"] = (
            self._identify_compression_opportunities()
        )

        logger.info(
            f"✅ Analysis complete: {analysis['total_files']} files, {analysis['total_directories']} directories"
        )
        return analysis

    def _get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file content"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def _identify_potential_merges(self) -> List[Dict[str, Any]]:
        """Identify files that could potentially be merged"""
        potential_merges = []

        # Look for similar files in same directory
        for root, dirs, files in os.walk(self.project_root):
            if "__pycache__" in root or ".venv" in root:
                continue

            # Group files by similarity
            file_groups = {}
            for file in files:
                if file.endswith(".py"):
                    base_name = file.replace(".py", "")
                    if base_name not in file_groups:
                        file_groups[base_name] = []
                    file_groups[base_name].append(file)

            # Check for potential merges
            for base_name, file_list in file_groups.items():
                if len(file_list) > 1:
                    potential_merges.append(
                        {
                            "directory": str(Path(root).relative_to(self.project_root)),
                            "base_name": base_name,
                            "files": file_list,
                            "merge_type": "similar_names",
                        }
                    )

        return potential_merges

    def _identify_compression_opportunities(self) -> List[Dict[str, Any]]:
        """Identify files that could be compressed"""
        compression_opportunities = []

        for root, dirs, files in os.walk(self.project_root):
            if "__pycache__" in root or ".venv" in root:
                continue

            for file in files:
                file_path = Path(root) / file
                file_size = file_path.stat().st_size
                file_suffix = file_path.suffix.lower()

                # Check for large text files that could be compressed
                if file_size > 100 * 1024 and file_suffix in [
                    ".txt",
                    ".md",
                    ".json",
                    ".log",
                ]:
                    compression_opportunities.append(
                        {
                            "file": str(file_path.relative_to(self.project_root)),
                            "size": file_size,
                            "size_mb": round(file_size / (1024 * 1024), 2),
                            "compression_type": "text_compression",
                        }
                    )

                # Check for large image/video files
                elif file_size > 5 * 1024 * 1024 and file_suffix in [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".mp4",
                    ".avi",
                ]:
                    compression_opportunities.append(
                        {
                            "file": str(file_path.relative_to(self.project_root)),
                            "size": file_size,
                            "size_mb": round(file_size / (1024 * 1024), 2),
                            "compression_type": "media_compression",
                        }
                    )

        return compression_opportunities

    def show_file_analysis(self, analysis: Dict[str, Any]):
        """Display file analysis results"""
        print("\n" + "=" * 80)
        print("📊 FRAMEWORK FILE ANALYSIS")
        print("=" * 80)

        print(f"\n📁 Project Structure:")
        print(f"   Total Files: {analysis['total_files']:,}")
        print(f"   Total Directories: {analysis['total_directories']:,}")

        print(f"\n📄 File Types:")
        for ext, info in sorted(
            analysis["file_types"].items(), key=lambda x: x[1]["count"], reverse=True
        ):
            size_mb = round(info["total_size"] / (1024 * 1024), 2)
            print(f"   {ext or 'no extension'}: {info['count']:,} files ({size_mb} MB)")

        if analysis["large_files"]:
            print(f"\n📦 Large Files (>1MB):")
            for file_info in sorted(
                analysis["large_files"], key=lambda x: x["size"], reverse=True
            )[:10]:
                print(f"   {file_info['path']}: {file_info['size_mb']} MB")

        if analysis["duplicate_files"]:
            print(f"\n🔄 Duplicate Files:")
            for dup in analysis["duplicate_files"][:5]:
                print(f"   {dup['original']} <-> {dup['duplicate']}")

        if analysis["potential_merges"]:
            print(f"\n🔗 Potential Merges:")
            for merge in analysis["potential_merges"][:5]:
                print(f"   {merge['directory']}/{merge['base_name']}: {merge['files']}")

        if analysis["compression_opportunities"]:
            print(f"\n🗜️ Compression Opportunities:")
            for comp in sorted(
                analysis["compression_opportunities"],
                key=lambda x: x["size"],
                reverse=True,
            )[:5]:
                print(
                    f"   {comp['file']}: {comp['size_mb']} MB ({comp['compression_type']})"
                )

    def compress_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Compress files based on analysis with backup"""
        # Create backup before compression
        backup_path = self.create_backup("compression")
        if not backup_path:
            return {"error": "Failed to create backup before compression"}

        logger.info("🗜️ Starting file compression...")

        compression_results = {
            "compressed_files": [],
            "saved_space": 0,
            "compression_ratio": 0.0,
            "backup_path": backup_path,
        }

        # Create compression directory
        compression_dir = self.project_root / "compressed"
        compression_dir.mkdir(exist_ok=True)

        for comp_opp in analysis["compression_opportunities"]:
            file_path = self.project_root / comp_opp["file"]

            if file_path.exists():
                try:
                    # Create compressed version
                    compressed_path = (
                        compression_dir
                        / f"{file_path.stem}_compressed{file_path.suffix}.gz"
                    )

                    with open(file_path, "rb") as f_in:
                        with gzip.open(compressed_path, "wb") as f_out:
                            shutil.copyfileobj(f_in, f_out)

                    # Calculate savings
                    original_size = file_path.stat().st_size
                    compressed_size = compressed_path.stat().st_size
                    saved_space = original_size - compressed_size

                    compression_results["compressed_files"].append(
                        {
                            "original": str(file_path.relative_to(self.project_root)),
                            "compressed": str(
                                compressed_path.relative_to(self.project_root)
                            ),
                            "original_size": original_size,
                            "compressed_size": compressed_size,
                            "saved_space": saved_space,
                            "compression_ratio": round(
                                (1 - compressed_size / original_size) * 100, 2
                            ),
                        }
                    )

                    compression_results["saved_space"] += saved_space

                except Exception as e:
                    logger.error(f"Failed to compress {file_path}: {e}")

        if compression_results["compressed_files"]:
            total_original = sum(
                f["original_size"] for f in compression_results["compressed_files"]
            )
            total_compressed = sum(
                f["compressed_size"] for f in compression_results["compressed_files"]
            )
            compression_results["compression_ratio"] = round(
                (1 - total_compressed / total_original) * 100, 2
            )

        logger.info(
            f"✅ Compression complete: {len(compression_results['compressed_files'])} files compressed"
        )
        return compression_results

    def merge_similar_files(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Merge similar files based on analysis with backup"""
        # Create backup before merging
        backup_path = self.create_backup("merging")
        if not backup_path:
            return {"error": "Failed to create backup before merging"}

        logger.info("🔗 Starting file merging...")

        merge_results = {
            "merged_files": [],
            "created_files": [],
            "saved_files": 0,
            "backup_path": backup_path,
        }

        for merge_opp in analysis["potential_merges"]:
            if merge_opp["merge_type"] == "similar_names":
                directory = self.project_root / merge_opp["directory"]
                base_name = merge_opp["base_name"]
                files = merge_opp["files"]

                if len(files) > 1:
                    try:
                        # Create merged file
                        merged_content = []
                        merged_content.append(f"# Merged from: {', '.join(files)}")
                        merged_content.append(
                            f"# Merged on: {datetime.now().isoformat()}"
                        )
                        merged_content.append("")

                        for file in files:
                            file_path = directory / file
                            if file_path.exists():
                                merged_content.append(f"# === {file} ===")
                                with open(file_path, "r", encoding="utf-8") as f:
                                    merged_content.append(f.read())
                                merged_content.append("")

                        # Write merged file
                        merged_file = directory / f"{base_name}_merged.py"
                        with open(merged_file, "w", encoding="utf-8") as f:
                            f.write("\n".join(merged_content))

                        merge_results["merged_files"].append(
                            {
                                "directory": merge_opp["directory"],
                                "base_name": base_name,
                                "original_files": files,
                                "merged_file": str(
                                    merged_file.relative_to(self.project_root)
                                ),
                            }
                        )

                        merge_results["created_files"].append(
                            str(merged_file.relative_to(self.project_root))
                        )
                        merge_results["saved_files"] += len(files) - 1

                    except Exception as e:
                        logger.error(
                            f"Failed to merge files in {merge_opp['directory']}: {e}"
                        )

        logger.info(
            f"✅ Merging complete: {len(merge_results['merged_files'])} groups merged"
        )
        return merge_results

    def cleanup_unused_files(self) -> Dict[str, Any]:
        """Clean up unused files and directories with backup"""
        # Create backup before cleanup
        backup_path = self.create_backup("cleanup")
        if not backup_path:
            return {"error": "Failed to create backup before cleanup"}

        logger.info("🧹 Starting cleanup...")

        cleanup_results = {
            "removed_files": [],
            "removed_directories": [],
            "saved_space": 0,
            "backup_path": backup_path,
        }

        # Remove __pycache__ directories
        for root, dirs, files in os.walk(self.project_root):
            if "__pycache__" in dirs:
                cache_dir = Path(root) / "__pycache__"
                try:
                    # Calculate size before removal
                    total_size = sum(
                        f.stat().st_size for f in cache_dir.rglob("*") if f.is_file()
                    )

                    shutil.rmtree(cache_dir)
                    cleanup_results["removed_directories"].append(
                        str(cache_dir.relative_to(self.project_root))
                    )
                    cleanup_results["saved_space"] += total_size

                except Exception as e:
                    logger.error(f"Failed to remove {cache_dir}: {e}")

        # Remove .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            try:
                size = pyc_file.stat().st_size
                pyc_file.unlink()
                cleanup_results["removed_files"].append(
                    str(pyc_file.relative_to(self.project_root))
                )
                cleanup_results["saved_space"] += size
            except Exception as e:
                logger.error(f"Failed to remove {pyc_file}: {e}")

        logger.info(
            f"✅ Cleanup complete: {len(cleanup_results['removed_files'])} files, {len(cleanup_results['removed_directories'])} directories removed"
        )
        return cleanup_results

    def show_compression_results(self, results: Dict[str, Any]):
        """Display compression results"""
        print("\n" + "=" * 80)
        print("🗜️ COMPRESSION RESULTS")
        print("=" * 80)

        if "error" in results:
            print(f"\n❌ Error: {results['error']}")
            return

        if results["compressed_files"]:
            print(f"\n📦 Compressed Files: {len(results['compressed_files'])}")
            for file_info in results["compressed_files"]:
                print(f"   {file_info['original']} -> {file_info['compressed']}")
                print(
                    f"     Size: {file_info['original_size']:,} -> {file_info['compressed_size']:,} bytes"
                )
                print(
                    f"     Saved: {file_info['saved_space']:,} bytes ({file_info['compression_ratio']}%)"
                )

            print(
                f"\n💾 Total Space Saved: {results['saved_space']:,} bytes ({results['compression_ratio']}%)"
            )
        else:
            print("\n📦 No files were compressed")

        if "backup_path" in results:
            print(f"\n💾 Backup created: {results['backup_path']}")

    def show_merge_results(self, results: Dict[str, Any]):
        """Display merge results"""
        print("\n" + "=" * 80)
        print("🔗 MERGE RESULTS")
        print("=" * 80)

        if "error" in results:
            print(f"\n❌ Error: {results['error']}")
            return

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

        if "backup_path" in results:
            print(f"\n💾 Backup created: {results['backup_path']}")

    def show_cleanup_results(self, results: Dict[str, Any]):
        """Display cleanup results"""
        print("\n" + "=" * 80)
        print("🧹 CLEANUP RESULTS")
        print("=" * 80)

        if "error" in results:
            print(f"\n❌ Error: {results['error']}")
            return

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

        if "backup_path" in results:
            print(f"\n💾 Backup created: {results['backup_path']}")

    def show_backup_list(self):
        """Display list of available backups"""
        backups = self.list_backups()

        print("\n" + "=" * 80)
        print("💾 AVAILABLE BACKUPS")
        print("=" * 80)

        if not backups:
            print("\n📭 No backups found")
            return

        print(f"\n📋 Found {len(backups)} backups:")
        for i, backup in enumerate(backups, 1):
            print(f"\n   {i}. {backup['id']}")
            print(f"      Created: {backup['created_readable']}")
            print(f"      Size: {backup['size_mb']} MB")
            print(f"      Path: {backup['path']}")

    def interactive_mode(self):
        """Run interactive CLI mode"""
        print("\n" + "=" * 80)
        print("🛠️ FRAMEWORK CLI - INTERACTIVE MODE")
        print("=" * 80)

        while True:
            print("\n📋 Available Commands:")
            print("  1. Analyze project structure")
            print("  2. Show file analysis")
            print("  3. Compress files")
            print("  4. Merge similar files")
            print("  5. Cleanup unused files")
            print("  6. Show all results")
            print("  7. Export analysis to JSON")
            print("  8. List backups")
            print("  9. Restore from backup")
            print("  10. Cleanup old backups")
            print("  11. Git status")
            print("  12. Git log")
            print("  13. Git workflow (add/commit/push)")
            print("  14. Git add files")
            print("  15. Git commit changes")
            print("  16. Git push changes")
            print("  17. Git pull changes")
            print("  18. Git branch management")
            print("  19. Git remote management")
            print("  0. Exit")

            choice = input("\n🔧 Enter your choice (0-19): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.analysis = self.analyze_project_structure()
                print("✅ Analysis complete!")
            elif choice == "2":
                if hasattr(self, "analysis"):
                    self.show_file_analysis(self.analysis)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "3":
                if hasattr(self, "analysis"):
                    self.compression_results = self.compress_files(self.analysis)
                    self.show_compression_results(self.compression_results)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "4":
                if hasattr(self, "analysis"):
                    self.merge_results = self.merge_similar_files(self.analysis)
                    self.show_merge_results(self.merge_results)
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "5":
                self.cleanup_results = self.cleanup_unused_files()
                self.show_cleanup_results(self.cleanup_results)
            elif choice == "6":
                if hasattr(self, "analysis"):
                    self.show_file_analysis(self.analysis)
                if hasattr(self, "compression_results"):
                    self.show_compression_results(self.compression_results)
                if hasattr(self, "merge_results"):
                    self.show_merge_results(self.merge_results)
                if hasattr(self, "cleanup_results"):
                    self.show_cleanup_results(self.cleanup_results)
            elif choice == "7":
                if hasattr(self, "analysis"):
                    self.export_analysis()
                else:
                    print("❌ Please run analysis first (option 1)")
            elif choice == "8":
                self.show_backup_list()
            elif choice == "9":
                backups = self.list_backups()
                if not backups:
                    print("❌ No backups available")
                    continue

                print("\n📋 Select backup to restore:")
                for i, backup in enumerate(backups, 1):
                    print(f"   {i}. {backup['id']} ({backup['created_readable']})")

                try:
                    backup_choice = int(input("\n🔧 Enter backup number: ")) - 1
                    if 0 <= backup_choice < len(backups):
                        backup_id = backups[backup_choice]["id"]
                        confirm = input(
                            f"\n⚠️ Are you sure you want to restore from {backup_id}? (y/N): "
                        )
                        if confirm.lower() == "y":
                            success = self.restore_backup(backup_id)
                            if success:
                                print("✅ Restore completed successfully!")
                            else:
                                print("❌ Restore failed!")
                        else:
                            print("❌ Restore cancelled")
                    else:
                        print("❌ Invalid backup number")
                except ValueError:
                    print("❌ Invalid input")
            elif choice == "10":
                keep_count = input(
                    "\n🔧 How many backups to keep? (default: 5): "
                ).strip()
                try:
                    keep_count = int(keep_count) if keep_count else 5
                    removed = self.cleanup_old_backups(keep_count)
                    print(f"✅ Cleanup complete: {removed} old backups removed")
                except ValueError:
                    print("❌ Invalid number")
            elif choice == "11":
                status = self.git_status()
                self.show_git_status(status)
            elif choice == "12":
                limit = input("\n🔧 How many commits to show? (default: 10): ").strip()
                try:
                    limit = int(limit) if limit else 10
                    log_result = self.git_log(limit)
                    self.show_git_log(log_result)
                except ValueError:
                    print("❌ Invalid number")
            elif choice == "13":
                message = input(
                    "\n🔧 Commit message (or press Enter for auto-message): "
                ).strip()
                workflow_result = self.git_workflow(message if message else None)
                if workflow_result["success"]:
                    print("✅ Git workflow completed successfully!")
                else:
                    print(
                        f"❌ Git workflow failed: {workflow_result.get('error', 'Unknown error')}"
                    )
            elif choice == "14":
                files_input = input(
                    "\n🔧 Files to add (comma-separated, or press Enter for all): "
                ).strip()
                files = (
                    [f.strip() for f in files_input.split(",")] if files_input else None
                )
                add_result = self.git_add(files)
                if add_result["success"]:
                    print("✅ Files added successfully!")
                else:
                    print(f"❌ Failed to add files: {add_result['stderr']}")
            elif choice == "15":
                message = input("\n🔧 Commit message: ").strip()
                if not message:
                    print("❌ Commit message is required")
                    continue
                files_input = input(
                    "\n🔧 Files to commit (comma-separated, or press Enter for staged): "
                ).strip()
                files = (
                    [f.strip() for f in files_input.split(",")] if files_input else None
                )
                commit_result = self.git_commit(message, files)
                if commit_result["success"]:
                    print("✅ Changes committed successfully!")
                else:
                    print(f"❌ Failed to commit: {commit_result['stderr']}")
            elif choice == "16":
                remote = (
                    input("\n🔧 Remote name (default: origin): ").strip() or "origin"
                )
                branch = (
                    input("\n🔧 Branch name (or press Enter for current): ").strip()
                    or None
                )
                push_result = self.git_push(remote, branch)
                if push_result["success"]:
                    print("✅ Changes pushed successfully!")
                else:
                    print(f"❌ Failed to push: {push_result['stderr']}")
            elif choice == "17":
                remote = (
                    input("\n🔧 Remote name (default: origin): ").strip() or "origin"
                )
                branch = (
                    input("\n🔧 Branch name (or press Enter for current): ").strip()
                    or None
                )
                pull_result = self.git_pull(remote, branch)
                if pull_result["success"]:
                    print("✅ Changes pulled successfully!")
                else:
                    print(f"❌ Failed to pull: {pull_result['stderr']}")
            elif choice == "18":
                print("\n📋 Branch Operations:")
                print("  1. List branches")
                print("  2. Create branch")
                print("  3. Delete branch")
                print("  4. Checkout branch")
                branch_choice = input("\n🔧 Enter branch operation (1-4): ").strip()

                if branch_choice == "1":
                    branch_result = self.git_branch("list")
                    if branch_result["success"]:
                        print("\n📋 Branches:")
                        branches = (
                            branch_result["stdout"].strip().split("\n")
                            if branch_result["stdout"]
                            else []
                        )
                        for branch in branches:
                            print(f"   {branch}")
                    else:
                        print(f"❌ Failed to list branches: {branch_result['stderr']}")
                elif branch_choice in ["2", "3", "4"]:
                    branch_name = input("\n🔧 Branch name: ").strip()
                    if not branch_name:
                        print("❌ Branch name is required")
                        continue

                    action_map = {"2": "create", "3": "delete", "4": "checkout"}
                    action = action_map[branch_choice]
                    branch_result = self.git_branch(action, branch_name)
                    if branch_result["success"]:
                        print(f"✅ Branch {action} completed successfully!")
                    else:
                        print(
                            f"❌ Failed to {action} branch: {branch_result['stderr']}"
                        )
                else:
                    print("❌ Invalid branch operation")
            elif choice == "19":
                print("\n📋 Remote Operations:")
                print("  1. List remotes")
                print("  2. Add remote")
                print("  3. Remove remote")
                remote_choice = input("\n🔧 Enter remote operation (1-3): ").strip()

                if remote_choice == "1":
                    remote_result = self.git_remote("list")
                    if remote_result["success"]:
                        print("\n📋 Remotes:")
                        remotes = (
                            remote_result["stdout"].strip().split("\n")
                            if remote_result["stdout"]
                            else []
                        )
                        for remote in remotes:
                            print(f"   {remote}")
                    else:
                        print(f"❌ Failed to list remotes: {remote_result['stderr']}")
                elif remote_choice in ["2", "3"]:
                    remote_name = input("\n🔧 Remote name: ").strip()
                    if not remote_name:
                        print("❌ Remote name is required")
                        continue

                    if remote_choice == "2":
                        remote_url = input("\n🔧 Remote URL: ").strip()
                        if not remote_url:
                            print("❌ Remote URL is required")
                            continue
                        remote_result = self.git_remote("add", remote_name, remote_url)
                    else:
                        remote_result = self.git_remote("remove", remote_name)

                    if remote_result["success"]:
                        print(
                            f"✅ Remote {remote_choice == '2' and 'added' or 'removed'} successfully!"
                        )
                    else:
                        print(f"❌ Failed to manage remote: {remote_result['stderr']}")
                else:
                    print("❌ Invalid remote operation")
            else:
                print("❌ Invalid choice. Please try again.")

    def export_analysis(self):
        """Export analysis results to JSON"""
        if hasattr(self, "analysis"):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "analysis": self.analysis,
            }

            if hasattr(self, "compression_results"):
                export_data["compression_results"] = self.compression_results

            if hasattr(self, "merge_results"):
                export_data["merge_results"] = self.merge_results

            if hasattr(self, "cleanup_results"):
                export_data["cleanup_results"] = self.cleanup_results

            export_file = self.project_root / "framework_analysis.json"
            with open(export_file, "w") as f:
                json.dump(export_data, f, indent=2)

            print(f"✅ Analysis exported to: {export_file}")

    def run_git_command(
        self, command: List[str], capture_output: bool = True
    ) -> Dict[str, Any]:
        """Run a git command and return results"""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=capture_output,
                text=True,
                timeout=30,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1,
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

    def git_status(self) -> Dict[str, Any]:
        """Get git repository status"""
        logger.info("📊 Checking git status...")

        # Check if this is a git repository
        git_check = self.run_git_command(["git", "rev-parse", "--git-dir"])
        if not git_check["success"]:
            return {"is_repo": False, "error": "Not a git repository"}

        # Get status
        status_result = self.run_git_command(["git", "status", "--porcelain"])
        branch_result = self.run_git_command(["git", "branch", "--show-current"])
        remote_result = self.run_git_command(["git", "remote", "-v"])

        # Parse status
        status_lines = (
            status_result["stdout"].strip().split("\n")
            if status_result["stdout"]
            else []
        )
        modified_files = []
        untracked_files = []
        staged_files = []

        for line in status_lines:
            if line:
                status_code = line[:2]
                file_path = line[3:]

                if status_code.startswith("M"):
                    staged_files.append(file_path)
                elif status_code.startswith(" M"):
                    modified_files.append(file_path)
                elif status_code.startswith("??"):
                    untracked_files.append(file_path)
                elif status_code.startswith("A"):
                    staged_files.append(file_path)
                elif status_code.startswith("D"):
                    staged_files.append(file_path)

        return {
            "is_repo": True,
            "current_branch": (
                branch_result["stdout"].strip()
                if branch_result["success"]
                else "unknown"
            ),
            "remotes": (
                remote_result["stdout"].strip().split("\n")
                if remote_result["success"]
                else []
            ),
            "modified_files": modified_files,
            "staged_files": staged_files,
            "untracked_files": untracked_files,
            "has_changes": bool(modified_files or staged_files or untracked_files),
        }

    def git_add(self, files: List[str] = None) -> Dict[str, Any]:
        """Add files to git staging area"""
        logger.info("📁 Adding files to git...")

        if files:
            # Add specific files
            command = ["git", "add"] + files
        else:
            # Add all files
            command = ["git", "add", "."]

        result = self.run_git_command(command)

        if result["success"]:
            logger.info("✅ Files added to staging area")
        else:
            logger.error(f"❌ Failed to add files: {result['stderr']}")

        return result

    def git_commit(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Commit staged changes"""
        logger.info("💾 Committing changes...")

        # Add files if specified
        if files:
            add_result = self.git_add(files)
            if not add_result["success"]:
                return add_result

        # Commit
        command = ["git", "commit", "-m", message]
        result = self.run_git_command(command)

        if result["success"]:
            logger.info("✅ Changes committed successfully")
        else:
            logger.error(f"❌ Failed to commit: {result['stderr']}")

        return result

    def git_push(self, remote: str = "origin", branch: str = None) -> Dict[str, Any]:
        """Push changes to remote repository"""
        logger.info("🚀 Pushing to remote...")

        if branch:
            command = ["git", "push", remote, branch]
        else:
            command = ["git", "push"]

        result = self.run_git_command(command)

        if result["success"]:
            logger.info("✅ Changes pushed successfully")
        else:
            logger.error(f"❌ Failed to push: {result['stderr']}")

        return result

    def git_pull(self, remote: str = "origin", branch: str = None) -> Dict[str, Any]:
        """Pull changes from remote repository"""
        logger.info("📥 Pulling from remote...")

        if branch:
            command = ["git", "pull", remote, branch]
        else:
            command = ["git", "pull"]

        result = self.run_git_command(command)

        if result["success"]:
            logger.info("✅ Changes pulled successfully")
        else:
            logger.error(f"❌ Failed to pull: {result['stderr']}")

        return result

    def git_branch(
        self, action: str = "list", branch_name: str = None
    ) -> Dict[str, Any]:
        """Manage git branches"""
        logger.info(f"🌿 Managing branches: {action}")

        if action == "list":
            command = ["git", "branch", "-a"]
        elif action == "create" and branch_name:
            command = ["git", "checkout", "-b", branch_name]
        elif action == "delete" and branch_name:
            command = ["git", "branch", "-d", branch_name]
        elif action == "checkout" and branch_name:
            command = ["git", "checkout", branch_name]
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Invalid branch action or missing branch name",
                "returncode": -1,
            }

        result = self.run_git_command(command)

        if result["success"]:
            logger.info(f"✅ Branch operation '{action}' completed successfully")
        else:
            logger.error(f"❌ Failed to {action} branch: {result['stderr']}")

        return result

    def git_log(self, limit: int = 10) -> Dict[str, Any]:
        """Get git commit history"""
        logger.info("📜 Getting git log...")

        command = ["git", "log", f"--oneline", f"-{limit}"]
        result = self.run_git_command(command)

        if result["success"]:
            commits = result["stdout"].strip().split("\n") if result["stdout"] else []
            logger.info(f"✅ Retrieved {len(commits)} commits")
        else:
            logger.error(f"❌ Failed to get git log: {result['stderr']}")

        return result

    def git_remote(
        self, action: str = "list", remote_name: str = None, remote_url: str = None
    ) -> Dict[str, Any]:
        """Manage git remotes"""
        logger.info(f"🌐 Managing remotes: {action}")

        if action == "list":
            command = ["git", "remote", "-v"]
        elif action == "add" and remote_name and remote_url:
            command = ["git", "remote", "add", remote_name, remote_url]
        elif action == "remove" and remote_name:
            command = ["git", "remote", "remove", remote_name]
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Invalid remote action or missing parameters",
                "returncode": -1,
            }

        result = self.run_git_command(command)

        if result["success"]:
            logger.info(f"✅ Remote operation '{action}' completed successfully")
        else:
            logger.error(f"❌ Failed to {action} remote: {result['stderr']}")

        return result

    def show_git_status(self, status: Dict[str, Any]):
        """Display git status information"""
        print("\n" + "=" * 80)
        print("🌿 GIT STATUS")
        print("=" * 80)

        if not status["is_repo"]:
            print(f"\n❌ {status['error']}")
            return

        print(f"\n📋 Repository Information:")
        print(f"   Current Branch: {status['current_branch']}")

        if status["remotes"]:
            print(f"   Remotes:")
            for remote in status["remotes"]:
                print(f"     {remote}")

        if status["has_changes"]:
            print(f"\n📝 Changes:")

            if status["staged_files"]:
                print(f"   📁 Staged Files ({len(status['staged_files'])}):")
                for file in status["staged_files"][:5]:  # Show first 5
                    print(f"     + {file}")
                if len(status["staged_files"]) > 5:
                    print(f"     ... and {len(status['staged_files']) - 5} more")

            if status["modified_files"]:
                print(f"   📝 Modified Files ({len(status['modified_files'])}):")
                for file in status["modified_files"][:5]:  # Show first 5
                    print(f"     ~ {file}")
                if len(status["modified_files"]) > 5:
                    print(f"     ... and {len(status['modified_files']) - 5} more")

            if status["untracked_files"]:
                print(f"   ❓ Untracked Files ({len(status['untracked_files'])}):")
                for file in status["untracked_files"][:5]:  # Show first 5
                    print(f"     ? {file}")
                if len(status["untracked_files"]) > 5:
                    print(f"     ... and {len(status['untracked_files']) - 5} more")
        else:
            print(f"\n✅ Working directory is clean")

    def show_git_log(self, log_result: Dict[str, Any]):
        """Display git log information"""
        print("\n" + "=" * 80)
        print("📜 GIT LOG")
        print("=" * 80)

        if log_result["success"]:
            commits = (
                log_result["stdout"].strip().split("\n") if log_result["stdout"] else []
            )
            print(f"\n📋 Recent Commits ({len(commits)}):")
            for i, commit in enumerate(commits, 1):
                print(f"   {i}. {commit}")
        else:
            print(f"\n❌ Failed to get git log: {log_result['stderr']}")

    def git_workflow(self, message: str = None) -> Dict[str, Any]:
        """Complete git workflow: add, commit, push"""
        logger.info("🔄 Running complete git workflow...")

        # Get current status
        status = self.git_status()
        if not status["is_repo"]:
            return {"success": False, "error": "Not a git repository"}

        if not status["has_changes"]:
            return {"success": False, "error": "No changes to commit"}

        # Add all files
        add_result = self.git_add()
        if not add_result["success"]:
            return add_result

        # Commit with message
        commit_message = (
            message or f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        commit_result = self.git_commit(commit_message)
        if not commit_result["success"]:
            return commit_result

        # Push to remote
        push_result = self.git_push()
        if not push_result["success"]:
            return push_result

        return {
            "success": True,
            "message": "Complete workflow executed successfully",
            "add_result": add_result,
            "commit_result": commit_result,
            "push_result": push_result,
        }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Framework CLI Management Tool")
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze project structure"
    )
    parser.add_argument("--compress", action="store_true", help="Compress files")
    parser.add_argument("--merge", action="store_true", help="Merge similar files")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup unused files")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("--export", action="store_true", help="Export analysis to JSON")
    parser.add_argument("--backup", action="store_true", help="Create backup only")
    parser.add_argument(
        "--list-backups", action="store_true", help="List available backups"
    )
    parser.add_argument("--restore", type=str, help="Restore from specific backup ID")
    parser.add_argument("--git-status", action="store_true", help="Show git status")
    parser.add_argument(
        "--git-log", type=int, metavar="LIMIT", help="Show git log (number of commits)"
    )
    parser.add_argument(
        "--git-workflow",
        type=str,
        metavar="MESSAGE",
        help="Run complete git workflow (add/commit/push)",
    )
    parser.add_argument(
        "--git-add",
        type=str,
        metavar="FILES",
        help="Add files to git (comma-separated)",
    )
    parser.add_argument(
        "--git-commit", type=str, metavar="MESSAGE", help="Commit changes with message"
    )
    parser.add_argument(
        "--git-push", action="store_true", help="Push changes to remote"
    )
    parser.add_argument(
        "--git-pull", action="store_true", help="Pull changes from remote"
    )
    parser.add_argument(
        "--git-branch",
        type=str,
        metavar="ACTION",
        help="Branch action (list/create/delete/checkout)",
    )
    parser.add_argument(
        "--git-remote",
        type=str,
        metavar="ACTION",
        help="Remote action (list/add/remove)",
    )

    args = parser.parse_args()

    cli = SimpleFrameworkCLI()

    if args.backup:
        backup_path = cli.create_backup("manual")
        if backup_path:
            print(f"✅ Backup created: {backup_path}")
        else:
            print("❌ Backup failed")
    elif args.list_backups:
        cli.show_backup_list()
    elif args.restore:
        success = cli.restore_backup(args.restore)
        if success:
            print("✅ Restore completed successfully!")
        else:
            print("❌ Restore failed!")
    elif args.git_status:
        status = cli.git_status()
        cli.show_git_status(status)
    elif args.git_log is not None:
        log_result = cli.git_log(args.git_log)
        cli.show_git_log(log_result)
    elif args.git_workflow is not None:
        workflow_result = cli.git_workflow(args.git_workflow)
        if workflow_result["success"]:
            print("✅ Git workflow completed successfully!")
        else:
            print(
                f"❌ Git workflow failed: {workflow_result.get('error', 'Unknown error')}"
            )
    elif args.git_add is not None:
        files = [f.strip() for f in args.git_add.split(",")] if args.git_add else None
        add_result = cli.git_add(files)
        if add_result["success"]:
            print("✅ Files added successfully!")
        else:
            print(f"❌ Failed to add files: {add_result['stderr']}")
    elif args.git_commit is not None:
        commit_result = cli.git_commit(args.git_commit)
        if commit_result["success"]:
            print("✅ Changes committed successfully!")
        else:
            print(f"❌ Failed to commit: {commit_result['stderr']}")
    elif args.git_push:
        push_result = cli.git_push()
        if push_result["success"]:
            print("✅ Changes pushed successfully!")
        else:
            print(f"❌ Failed to push: {push_result['stderr']}")
    elif args.git_pull:
        pull_result = cli.git_pull()
        if pull_result["success"]:
            print("✅ Changes pulled successfully!")
        else:
            print(f"❌ Failed to pull: {pull_result['stderr']}")
    elif args.git_branch is not None:
        if args.git_branch == "list":
            branch_result = cli.git_branch("list")
            if branch_result["success"]:
                print("\n📋 Branches:")
                branches = (
                    branch_result["stdout"].strip().split("\n")
                    if branch_result["stdout"]
                    else []
                )
                for branch in branches:
                    print(f"   {branch}")
            else:
                print(f"❌ Failed to list branches: {branch_result['stderr']}")
        else:
            print(
                f"❌ Branch action '{args.git_branch}' not supported in command line mode"
            )
            print("   Use interactive mode for create/delete/checkout operations")
    elif args.git_remote is not None:
        if args.git_remote == "list":
            remote_result = cli.git_remote("list")
            if remote_result["success"]:
                print("\n📋 Remotes:")
                remotes = (
                    remote_result["stdout"].strip().split("\n")
                    if remote_result["stdout"]
                    else []
                )
                for remote in remotes:
                    print(f"   {remote}")
            else:
                print(f"❌ Failed to list remotes: {remote_result['stderr']}")
        else:
            print(
                f"❌ Remote action '{args.git_remote}' not supported in command line mode"
            )
            print("   Use interactive mode for add/remove operations")
    elif args.interactive:
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
