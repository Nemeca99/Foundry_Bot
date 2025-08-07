#!/usr/bin/env python3
"""
System Cleanup Script - Safe and Smart
Removes duplicates, clears temp files, optimizes storage
"""

import os
import hashlib
import shutil
import json
import time
from pathlib import Path
from collections import defaultdict
import psutil
import subprocess
from datetime import datetime


class SystemCleanup:
    def __init__(self):
        self.duplicates_found = defaultdict(list)
        self.files_processed = 0
        self.space_freed = 0
        self.cleanup_log = []

    def log_action(self, action, details):
        """Log cleanup actions"""
        timestamp = datetime.now().isoformat()
        self.cleanup_log.append(
            {"timestamp": timestamp, "action": action, "details": details}
        )
        print(f"✅ {action}: {details}")

    def get_file_hash(self, filepath, chunk_size=8192):
        """Get MD5 hash of file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None

    def find_duplicates(self, directory, extensions=None):
        """Find duplicate files by content hash"""
        print(f"🔍 Scanning {directory} for duplicates...")

        if extensions:
            extensions = [ext.lower() for ext in extensions]

        file_hashes = defaultdict(list)

        for root, dirs, files in os.walk(directory):
            # Skip system directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["$Recycle.Bin", "System Volume Information"]
            ]

            for filename in files:
                filepath = os.path.join(root, filename)

                # Skip if extension filter is set
                if extensions:
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext not in extensions:
                        continue

                try:
                    file_hash = self.get_file_hash(filepath)
                    if file_hash:
                        file_hashes[file_hash].append(filepath)
                        self.files_processed += 1

                        if self.files_processed % 100 == 0:
                            print(f"   Processed {self.files_processed} files...")

                except Exception as e:
                    continue

        # Find duplicates
        for file_hash, file_list in file_hashes.items():
            if len(file_list) > 1:
                # Sort by path length (keep shortest path)
                file_list.sort(key=len)
                original = file_list[0]
                duplicates = file_list[1:]

                self.duplicates_found[file_hash] = {
                    "original": original,
                    "duplicates": duplicates,
                    "size": (
                        os.path.getsize(original) if os.path.exists(original) else 0
                    ),
                }

        return self.duplicates_found

    def remove_duplicates(self, dry_run=True):
        """Remove duplicate files (dry run by default)"""
        total_space = 0
        files_to_remove = []

        for file_hash, file_info in self.duplicates_found.items():
            original = file_info["original"]
            duplicates = file_info["duplicates"]
            size = file_info["size"]

            print(f"\n📁 Original: {original}")
            print(f"   Size: {self.format_size(size)}")
            print(f"   Duplicates found: {len(duplicates)}")

            for dup in duplicates:
                print(f"   🗑️  Duplicate: {dup}")
                if not dry_run:
                    try:
                        os.remove(dup)
                        total_space += size
                        self.log_action("Removed duplicate", dup)
                    except Exception as e:
                        print(f"   ❌ Failed to remove {dup}: {e}")
                else:
                    files_to_remove.append(dup)
                    total_space += size

        if dry_run:
            print(f"\n🔍 DRY RUN - Would free: {self.format_size(total_space)}")
            print(f"   Files that would be removed: {len(files_to_remove)}")
        else:
            print(f"\n✅ Removed duplicates - Freed: {self.format_size(total_space)}")
            self.space_freed += total_space

        return total_space

    def clear_temp_files(self, dry_run=True):
        """Clear temporary files"""
        temp_dirs = [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            r"C:\Windows\Temp",
            r"C:\Users\%USERNAME%\AppData\Local\Temp",
        ]

        total_cleared = 0

        for temp_dir in temp_dirs:
            if not temp_dir:
                continue

            temp_dir = os.path.expandvars(temp_dir)
            if not os.path.exists(temp_dir):
                continue

            print(f"🧹 Cleaning {temp_dir}...")

            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            if os.path.exists(filepath):
                                size = os.path.getsize(filepath)
                                if not dry_run:
                                    os.remove(filepath)
                                    total_cleared += size
                                    self.log_action("Removed temp file", filepath)
                        except:
                            continue
            except Exception as e:
                print(f"   ⚠️  Error cleaning {temp_dir}: {e}")

        if dry_run:
            print(f"🔍 DRY RUN - Would clear: {self.format_size(total_cleared)}")
        else:
            print(f"✅ Cleared temp files - Freed: {self.format_size(total_cleared)}")
            self.space_freed += total_cleared

        return total_cleared

    def clear_browser_cache(self, dry_run=True):
        """Clear browser cache files"""
        browsers = {
            "Chrome": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache",
            "Edge": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache",
            "Firefox": r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles",
        }

        total_cleared = 0

        for browser, cache_path in browsers.items():
            cache_path = os.path.expandvars(cache_path)
            if os.path.exists(cache_path):
                print(f"🌐 Cleaning {browser} cache...")

                try:
                    for root, dirs, files in os.walk(cache_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                if os.path.exists(filepath):
                                    size = os.path.getsize(filepath)
                                    if not dry_run:
                                        os.remove(filepath)
                                        total_cleared += size
                                        self.log_action(
                                            f"Removed {browser} cache", filepath
                                        )
                            except:
                                continue
                except Exception as e:
                    print(f"   ⚠️  Error cleaning {browser}: {e}")

        if dry_run:
            print(
                f"🔍 DRY RUN - Would clear browser cache: {self.format_size(total_cleared)}"
            )
        else:
            print(
                f"✅ Cleared browser cache - Freed: {self.format_size(total_cleared)}"
            )
            self.space_freed += total_cleared

        return total_cleared

    def analyze_disk_usage(self, directory):
        """Analyze disk usage by directory"""
        print(f"📊 Analyzing disk usage in {directory}...")

        dir_sizes = {}

        try:
            for root, dirs, files in os.walk(directory):
                total_size = 0
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        if os.path.exists(filepath):
                            total_size += os.path.getsize(filepath)
                    except:
                        continue

                if total_size > 100 * 1024 * 1024:  # Only show dirs > 100MB
                    dir_sizes[root] = total_size

            # Sort by size
            sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)

            print(f"\n📁 Largest directories in {directory}:")
            for path, size in sorted_dirs[:10]:
                print(f"   {self.format_size(size)} - {path}")

        except Exception as e:
            print(f"   ⚠️  Error analyzing {directory}: {e}")

    def format_size(self, bytes):
        """Format bytes into human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

    def save_cleanup_report(self, filename="cleanup_report.json"):
        """Save cleanup report to file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_processed": self.files_processed,
            "duplicates_found": len(self.duplicates_found),
            "space_freed": self.space_freed,
            "cleanup_log": self.cleanup_log,
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"📄 Cleanup report saved to: {filename}")

    def run_full_cleanup(self, directories=None, dry_run=True):
        """Run full cleanup process"""
        print("🧹 SYSTEM CLEANUP STARTING")
        print("=" * 50)

        if directories is None:
            directories = ["C:\\Users", "D:\\", "E:\\"]

        # Step 1: Find duplicates
        for directory in directories:
            if os.path.exists(directory):
                self.find_duplicates(
                    directory,
                    extensions=[
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".mp4",
                        ".avi",
                        ".mkv",
                        ".pdf",
                        ".doc",
                        ".docx",
                    ],
                )

        # Step 2: Remove duplicates
        duplicate_space = self.remove_duplicates(dry_run)

        # Step 3: Clear temp files
        temp_space = self.clear_temp_files(dry_run)

        # Step 4: Clear browser cache
        browser_space = self.clear_browser_cache(dry_run)

        # Step 5: Analyze disk usage
        for directory in directories:
            if os.path.exists(directory):
                self.analyze_disk_usage(directory)

        total_space = duplicate_space + temp_space + browser_space

        print("\n" + "=" * 50)
        print("📊 CLEANUP SUMMARY")
        print("=" * 50)
        print(f"Files processed: {self.files_processed:,}")
        print(f"Duplicates found: {len(self.duplicates_found)}")
        print(f"Total space that could be freed: {self.format_size(total_space)}")

        if not dry_run:
            self.space_freed = total_space
            self.save_cleanup_report()

        return total_space


def main():
    cleanup = SystemCleanup()

    print("🧹 System Cleanup Tool")
    print("This will help free up space safely")
    print("\nOptions:")
    print("1. Dry run (see what would be cleaned)")
    print("2. Full cleanup (actually remove files)")
    print("3. Just find duplicates")
    print("4. Just clear temp files")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        print("\n🔍 Running DRY RUN - no files will be deleted")
        cleanup.run_full_cleanup(dry_run=True)

    elif choice == "2":
        confirm = input("\n⚠️  This will actually delete files. Continue? (y/N): ")
        if confirm.lower() == "y":
            cleanup.run_full_cleanup(dry_run=False)
        else:
            print("Cancelled.")

    elif choice == "3":
        directories = input("Enter directories to scan (comma separated): ").strip()
        if directories:
            dir_list = [d.strip() for d in directories.split(",")]
            for directory in dir_list:
                if os.path.exists(directory):
                    cleanup.find_duplicates(directory)
            cleanup.remove_duplicates(dry_run=True)

    elif choice == "4":
        cleanup.clear_temp_files(dry_run=True)
        confirm = input("Clear temp files? (y/N): ")
        if confirm.lower() == "y":
            cleanup.clear_temp_files(dry_run=False)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
