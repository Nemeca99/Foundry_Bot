#!/usr/bin/env python3
"""
Launch Script
Easy launcher for all AI Writing Companion components
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def launch_system_dashboard():
    """Launch the system dashboard"""
    from core.system_dashboard import main
    main()

def launch_analytics_dashboard():
    """Launch the analytics dashboard"""
    from core.analytics_dashboard import main
    main()

def launch_project_manager():
    """Launch the project manager"""
    from core.project_manager import main
    main()

def launch_discord_bot():
    """Launch the Discord bot"""
    import subprocess
    subprocess.run([sys.executable, "scripts/start_bot.py"])

def launch_tests():
    """Launch the test suite"""
    import subprocess
    subprocess.run([sys.executable, "scripts/run_tests.py"])

def show_help():
    """Show help information"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           AI WRITING COMPANION LAUNCHER                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Available Commands:
────────────────────────────────────────────────────────────────────────────────

📊 System Management:
  python launch.py dashboard     - Launch system dashboard
  python launch.py analytics     - Launch analytics dashboard
  python launch.py projects      - Launch project manager

🤖 Bot Management:
  python launch.py bot           - Start Discord bot
  python launch.py tests         - Run test suite

📚 Documentation:
  python launch.py docs          - Open documentation directory
  python launch.py help          - Show this help message

Examples:
  python launch.py dashboard --monitor --interval 60
  python launch.py analytics --system-report --period month
  python launch.py projects --list
  python launch.py bot

For detailed help on each component:
  python launch.py dashboard --help
  python launch.py analytics --help
  python launch.py projects --help
""")

def main():
    """Main launcher function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "dashboard":
        launch_system_dashboard()
    elif command == "analytics":
        launch_analytics_dashboard()
    elif command == "projects":
        launch_project_manager()
    elif command == "bot":
        launch_discord_bot()
    elif command == "tests":
        launch_tests()
    elif command == "docs":
        import subprocess
        subprocess.run(["explorer", "docs"])
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main() 