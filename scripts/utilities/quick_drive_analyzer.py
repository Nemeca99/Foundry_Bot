#!/usr/bin/env python3
"""
Quick Drive Analyzer - See What's Taking Up Space
Fast analysis without full file scanning
"""

import os
import psutil
from pathlib import Path
import subprocess

def analyze_drive_space():
    """Quick analysis of drive space usage"""
    print("📊 QUICK DRIVE ANALYSIS")
    print("=" * 50)
    
    drives = {
        'C:': 'System/Programs',
        'D:': 'AI/Work (Target)',
        'E:': 'Backup/Storage (2TB)',
        'F:': 'Additional Storage',
        'G:': 'Additional Storage'
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
            
            # Color coding based on usage
            if percent > 90:
                print(f"   ⚠️  CRITICAL: {percent:.1f}% full!")
            elif percent > 80:
                print(f"   ⚠️  WARNING: {percent:.1f}% full")
            elif percent > 70:
                print(f"   ⚠️  Getting full: {percent:.1f}%")
            else:
                print(f"   ✅ Good: {percent:.1f}% used")
                
        except Exception as e:
            print(f"   ❌ Error analyzing {drive}: {e}")

def get_largest_directories(drive, limit=10):
    """Get largest directories on a drive using PowerShell"""
    print(f"\n📁 Largest directories on {drive}:")
    print("-" * 40)
    
    try:
        # PowerShell command to get directory sizes
        cmd = f'Get-ChildItem {drive} -Directory -ErrorAction SilentlyContinue | ForEach-Object {{ $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum; [PSCustomObject]@{{ Path = $_.FullName; Size = $size }} }} | Sort-Object Size -Descending | Select-Object -First {limit} | ForEach-Object {{ "{0} - {1:N0} bytes" -f $_.Path, $_.Size }}'
        
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"   ⚠️  Could not analyze {drive} directories")
            
    except Exception as e:
        print(f"   ❌ Error analyzing {drive} directories: {e}")

def format_size(bytes):
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def get_process_memory_usage():
    """Get top memory-using processes"""
    print(f"\n💾 Top Memory-Using Processes:")
    print("-" * 40)
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                processes.append({
                    'name': proc.info['name'],
                    'memory_mb': proc.info['memory_info'].rss / (1024 * 1024)
                })
            except:
                continue
        
        # Sort by memory usage
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        
        for i, proc in enumerate(processes[:10]):
            print(f"   {i+1:2d}. {proc['name']:<20} {proc['memory_mb']:>8.1f} MB")
            
    except Exception as e:
        print(f"   ❌ Error getting process info: {e}")

def main():
    print("🚀 Quick Drive Analyzer")
    print("Fast analysis of your storage situation")
    
    # Analyze drive space
    analyze_drive_space()
    
    # Get largest directories on C: (most important)
    get_largest_directories('C:', 5)
    
    # Get process memory usage
    get_process_memory_usage()
    
    print("\n" + "=" * 50)
    print("💡 RECOMMENDATIONS:")
    print("=" * 50)
    print("• C: is 88% full - move large files to E: (2TB)")
    print("• D: has 347GB free - perfect for AI/work files")
    print("• E: has 1.2TB free - great for storage/backup")
    print("• Consider moving:")
    print("  - Downloads folder to E:")
    print("  - Large media files to E:")
    print("  - AI models to D:")
    print("  - Development projects to D:")
    
    print(f"\n🎯 Next steps:")
    print("1. Run 'python storage_migration.py' to organize files")
    print("2. Run 'python system_cleanup.py' to remove duplicates")
    print("3. Move LM Studio models to D: drive")

if __name__ == "__main__":
    main() 