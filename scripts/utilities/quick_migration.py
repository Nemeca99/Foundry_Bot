#!/usr/bin/env python3
"""
Quick Migration Script - Automatic File Organization
Moves AI/work files to D:, everything else to E:
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import psutil

def analyze_drive_usage():
    """Quick analysis of drive space"""
    print("📊 DRIVE ANALYSIS")
    print("=" * 40)
    
    drives = {
        'C:': 'System/Programs',
        'D:': 'AI/Work (Target)',
        'E:': 'Backup/Storage (2TB)',
    }
    
    for drive, purpose in drives.items():
        try:
            usage = psutil.disk_usage(f"{drive}\\")
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            percent = (usage.used / usage.total) * 100
            
            print(f"\n{drive} Drive ({purpose}):")
            print(f"   Total: {total_gb:.1f} GB")
            print(f"   Used: {used_gb:.1f} GB ({percent:.1f}%)")
            print(f"   Free: {free_gb:.1f} GB")
            
        except Exception as e:
            print(f"   ❌ Error analyzing {drive}: {e}")

def find_ai_work_files():
    """Find AI and work-related files in common locations"""
    ai_locations = [
        r"C:\Users\nemec\Downloads",
        r"C:\Users\nemec\Documents",
        r"C:\Users\nemec\Desktop",
        r"D:\Simulacra_Rancher_Project",
        r"C:\Users\nemec\AppData\Local\LM Studio",
        r"C:\Users\nemec\AppData\Roaming\LM Studio",
    ]
    
    ai_extensions = {
        '.py', '.ipynb', '.json', '.yaml', '.yml', '.txt', '.md',
        '.model', '.bin', '.safetensors', '.gguf', '.ggml',
        '.db', '.sqlite', '.csv', '.tsv', '.parquet',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
        '.mp4', '.avi', '.mkv', '.mov', '.wmv',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx',
        '.zip', '.rar', '.7z', '.tar', '.gz'
    }
    
    ai_files = []
    other_files = []
    
    print("🔍 Scanning for AI/work files...")
    
    for location in ai_locations:
        if not os.path.exists(location):
            continue
            
        print(f"   Scanning: {location}")
        
        try:
            for root, dirs, files in os.walk(location):
                # Skip system directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d not in ['$Recycle.Bin', 'System Volume Information']]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    # Check if it's an AI/work file
                    is_ai_file = False
                    
                    # Check extension
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ai_extensions:
                        is_ai_file = True
                    
                    # Check filename for keywords
                    filename_lower = file.lower()
                    ai_keywords = ['ai', 'ml', 'model', 'dataset', 'llm', 'gpt', 'claude', 
                                 'dolphin', 'mistral', 'tensor', 'pytorch', 'transformers',
                                 'huggingface', 'ollama', 'lmstudio', 'simulacra', 'rancher',
                                 'discord', 'bot', 'project', 'work', 'development', 'code']
                    
                    for keyword in ai_keywords:
                        if keyword in filename_lower:
                            is_ai_file = True
                            break
                    
                    try:
                        size = os.path.getsize(filepath)
                        file_info = {
                            'path': filepath,
                            'size': size,
                            'relative_path': os.path.relpath(filepath, location)
                        }
                        
                        if is_ai_file:
                            ai_files.append(file_info)
                        else:
                            other_files.append(file_info)
                            
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"   ⚠️  Error scanning {location}: {e}")
    
    return ai_files, other_files

def migrate_files(files, target_dir, dry_run=True):
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
                print(f"✅ Moved: {relative_path}")
            else:
                print(f"   Would move: {relative_path}")
                total_moved += file_info['size']
                files_moved += 1
                
        except Exception as e:
            print(f"   ❌ Error moving {relative_path}: {e}")
    
    if dry_run:
        print(f"\n🔍 DRY RUN - Would move {files_moved} files ({format_size(total_moved)})")
    else:
        print(f"\n✅ Moved {files_moved} files ({format_size(total_moved)})")
    
    return total_moved

def format_size(bytes):
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def main():
    print("🚀 Quick Storage Migration")
    print("=" * 40)
    
    # Analyze drives
    analyze_drive_usage()
    
    # Find files
    ai_files, other_files = find_ai_work_files()
    
    # Show plan
    ai_total = sum(f['size'] for f in ai_files)
    other_total = sum(f['size'] for f in other_files)
    
    print(f"\n📋 MIGRATION PLAN")
    print("=" * 40)
    print(f"🎯 AI/Work Files (Move to D:): {len(ai_files):,} files ({format_size(ai_total)})")
    print(f"📦 Other Files (Move to E:): {len(other_files):,} files ({format_size(other_total)})")
    
    # Show some examples
    if ai_files:
        print(f"\n📁 Sample AI/Work files:")
        for file in ai_files[:3]:
            print(f"   {file['relative_path']} ({format_size(file['size'])})")
    
    if other_files:
        print(f"\n📁 Sample other files:")
        for file in other_files[:3]:
            print(f"   {file['relative_path']} ({format_size(file['size'])})")
    
    # Ask for confirmation
    print(f"\n⚠️  This will move files. Continue? (y/N): ", end="")
    confirm = input().strip().lower()
    
    if confirm == 'y':
        print(f"\n🎯 Migrating AI/Work files to D:\\AI_Work\\")
        ai_space = migrate_files(ai_files, "D:\\AI_Work\\", dry_run=False)
        
        print(f"\n📦 Migrating other files to E:\\Storage\\")
        other_space = migrate_files(other_files, "E:\\Storage\\", dry_run=False)
        
        total_space = ai_space + other_space
        
        print(f"\n✅ MIGRATION COMPLETE")
        print("=" * 40)
        print(f"AI/Work files moved: {len(ai_files):,} ({format_size(ai_space)})")
        print(f"Other files moved: {len(other_files):,} ({format_size(other_space)})")
        print(f"Total space migrated: {format_size(total_space)}")
        
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main() 