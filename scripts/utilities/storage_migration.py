#!/usr/bin/env python3
"""
Storage Migration Script - Organize Your Drives
Move AI/work to D:, everything else to E: (2TB backup)
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import psutil

class StorageMigration:
    def __init__(self):
        self.migration_log = []
        self.files_moved = 0
        self.space_freed = 0
        
    def log_action(self, action, details):
        """Log migration actions"""
        timestamp = datetime.now().isoformat()
        self.migration_log.append({
            "timestamp": timestamp,
            "action": action,
            "details": details
        })
        print(f"✅ {action}: {details}")
    
    def analyze_drive_usage(self):
        """Analyze current drive usage"""
        print("📊 ANALYZING DRIVE USAGE")
        print("=" * 50)
        
        drives = {
            'C:': {'path': 'C:\\', 'purpose': 'System/Programs'},
            'D:': {'path': 'D:\\', 'purpose': 'AI/Work (Target)'},
            'E:': {'path': 'E:\\', 'purpose': 'Backup/Storage (2TB)'},
            'F:': {'path': 'F:\\', 'purpose': 'Additional Storage'},
            'G:': {'path': 'G:\\', 'purpose': 'Additional Storage'}
        }
        
        for drive, info in drives.items():
            try:
                usage = psutil.disk_usage(info['path'])
                free_gb = usage.free / (1024**3)
                total_gb = usage.total / (1024**3)
                used_gb = usage.used / (1024**3)
                percent = (usage.used / usage.total) * 100
                
                print(f"\n{drive} Drive ({info['purpose']}):")
                print(f"   Total: {total_gb:.1f} GB")
                print(f"   Used: {used_gb:.1f} GB ({percent:.1f}%)")
                print(f"   Free: {free_gb:.1f} GB")
                
            except Exception as e:
                print(f"   ❌ Error analyzing {drive}: {e}")
    
    def identify_ai_work_files(self, source_dir):
        """Identify AI and work-related files"""
        ai_extensions = {
            '.py', '.ipynb', '.json', '.yaml', '.yml', '.txt', '.md',
            '.model', '.bin', '.safetensors', '.gguf', '.ggml',
            '.db', '.sqlite', '.csv', '.tsv', '.parquet',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
            '.mp4', '.avi', '.mkv', '.mov', '.wmv',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.zip', '.rar', '.7z', '.tar', '.gz'
        }
        
        ai_keywords = {
            'ai', 'ml', 'machine', 'learning', 'neural', 'model',
            'dataset', 'training', 'inference', 'embedding',
            'llm', 'gpt', 'claude', 'dolphin', 'mistral',
            'tensor', 'pytorch', 'torch', 'transformers',
            'huggingface', 'ollama', 'lmstudio',
            'simulacra', 'rancher', 'astra', 'lyra',
            'discord', 'bot', 'discord.py',
            'project', 'work', 'development', 'code'
        }
        
        ai_files = []
        other_files = []
        
        print(f"🔍 Scanning {source_dir} for AI/work files...")
        
        for root, dirs, files in os.walk(source_dir):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['$Recycle.Bin', 'System Volume Information', 'Windows']]
            
            for file in files:
                filepath = os.path.join(root, file)
                filename_lower = file.lower()
                
                # Check if it's an AI/work file
                is_ai_file = False
                
                # Check extension
                ext = os.path.splitext(file)[1].lower()
                if ext in ai_extensions:
                    is_ai_file = True
                
                # Check filename for keywords
                for keyword in ai_keywords:
                    if keyword in filename_lower:
                        is_ai_file = True
                        break
                
                # Check if it's in common AI directories
                path_lower = filepath.lower()
                ai_dirs = ['ai', 'ml', 'models', 'datasets', 'projects', 'work', 
                          'development', 'code', 'simulacra', 'rancher', 'discord']
                for ai_dir in ai_dirs:
                    if ai_dir in path_lower:
                        is_ai_file = True
                        break
                
                try:
                    size = os.path.getsize(filepath)
                    file_info = {
                        'path': filepath,
                        'size': size,
                        'relative_path': os.path.relpath(filepath, source_dir)
                    }
                    
                    if is_ai_file:
                        ai_files.append(file_info)
                    else:
                        other_files.append(file_info)
                        
                except Exception as e:
                    continue
        
        return ai_files, other_files
    
    def suggest_migration_plan(self, ai_files, other_files):
        """Suggest what to move where"""
        print("\n📋 MIGRATION PLAN")
        print("=" * 50)
        
        # Calculate sizes
        ai_total = sum(f['size'] for f in ai_files)
        other_total = sum(f['size'] for f in other_files)
        
        print(f"\n🎯 AI/Work Files (Move to D:):")
        print(f"   Files: {len(ai_files):,}")
        print(f"   Size: {self.format_size(ai_total)}")
        
        print(f"\n📦 Other Files (Move to E:):")
        print(f"   Files: {len(other_files):,}")
        print(f"   Size: {self.format_size(other_total)}")
        
        # Show some examples
        print(f"\n📁 Sample AI/Work files:")
        for file in ai_files[:5]:
            print(f"   {file['relative_path']} ({self.format_size(file['size'])})")
        
        print(f"\n📁 Sample other files:")
        for file in other_files[:5]:
            print(f"   {file['relative_path']} ({self.format_size(file['size'])})")
        
        return ai_files, other_files
    
    def migrate_files(self, files, target_dir, dry_run=True):
        """Migrate files to target directory"""
        if not os.path.exists(target_dir):
            if not dry_run:
                os.makedirs(target_dir, exist_ok=True)
            print(f"📁 Would create directory: {target_dir}")
        
        total_moved = 0
        files_moved = 0
        
        for file_info in files:
            source_path = file_info['path']
            relative_path = file_info['relative_path']
            target_path = os.path.join(target_dir, relative_path)
            
            # Create target directory if needed
            target_dir_path = os.path.dirname(target_path)
            if not dry_run and not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path, exist_ok=True)
            
            try:
                if not dry_run:
                    shutil.move(source_path, target_path)
                    total_moved += file_info['size']
                    files_moved += 1
                    self.log_action("Moved file", f"{relative_path} -> {target_path}")
                else:
                    print(f"   Would move: {relative_path} -> {target_path}")
                    total_moved += file_info['size']
                    files_moved += 1
                    
            except Exception as e:
                print(f"   ❌ Error moving {relative_path}: {e}")
        
        if dry_run:
            print(f"\n🔍 DRY RUN - Would move {files_moved} files ({self.format_size(total_moved)})")
        else:
            print(f"\n✅ Moved {files_moved} files ({self.format_size(total_moved)})")
            self.space_freed += total_moved
        
        return total_moved
    
    def format_size(self, bytes):
        """Format bytes into human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def save_migration_report(self, filename="migration_report.json"):
        """Save migration report to file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_moved": self.files_moved,
            "space_freed": self.space_freed,
            "migration_log": self.migration_log
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Migration report saved to: {filename}")
    
    def run_migration(self, source_dir, dry_run=True):
        """Run the full migration process"""
        print("🚀 STORAGE MIGRATION STARTING")
        print("=" * 50)
        
        # Step 1: Analyze current drive usage
        self.analyze_drive_usage()
        
        # Step 2: Identify AI/work files
        ai_files, other_files = self.identify_ai_work_files(source_dir)
        
        # Step 3: Suggest migration plan
        self.suggest_migration_plan(ai_files, other_files)
        
        # Step 4: Migrate AI files to D:
        print(f"\n🎯 Migrating AI/Work files to D:\\AI_Work\\")
        ai_space = self.migrate_files(ai_files, "D:\\AI_Work\\", dry_run)
        
        # Step 5: Migrate other files to E:
        print(f"\n📦 Migrating other files to E:\\Storage\\")
        other_space = self.migrate_files(other_files, "E:\\Storage\\", dry_run)
        
        total_space = ai_space + other_space
        
        print("\n" + "=" * 50)
        print("📊 MIGRATION SUMMARY")
        print("=" * 50)
        print(f"AI/Work files: {len(ai_files):,} ({self.format_size(ai_space)})")
        print(f"Other files: {len(other_files):,} ({self.format_size(other_space)})")
        print(f"Total space to migrate: {self.format_size(total_space)}")
        
        if not dry_run:
            self.space_freed = total_space
            self.save_migration_report()
        
        return total_space

def main():
    migration = StorageMigration()
    
    print("🚀 Storage Migration Tool")
    print("Organize your drives: AI/Work -> D:, Everything else -> E:")
    print("\nOptions:")
    print("1. Analyze and plan (dry run)")
    print("2. Full migration (actually move files)")
    print("3. Just analyze drive usage")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🔍 Running DRY RUN - no files will be moved")
        source = input("Enter source directory to scan (default: C:\\Users): ").strip()
        if not source:
            source = "C:\\Users"
        migration.run_migration(source, dry_run=True)
        
    elif choice == "2":
        confirm = input("\n⚠️  This will actually move files. Continue? (y/N): ")
        if confirm.lower() == 'y':
            source = input("Enter source directory to scan (default: C:\\Users): ").strip()
            if not source:
                source = "C:\\Users"
            migration.run_migration(source, dry_run=False)
        else:
            print("Cancelled.")
            
    elif choice == "3":
        migration.analyze_drive_usage()
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main() 