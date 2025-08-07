#!/usr/bin/env python3
"""
Foundry Bot - Main Entry Point
==============================

This is the main entry point for starting the Discord bot.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import queue manager
from framework.queue_manager import QueueProcessor, QueueManager


class BotLauncher(QueueProcessor):
    """Bot launcher with queue system integration"""

    def __init__(self):
        super().__init__("bot_launcher")
        self.queue_manager = QueueManager()
        self.bot_instance = None

    def _process_item(self, item):
        """Process queue items for bot launcher operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")

            if operation_type == "start_bot":
                return self._handle_start_bot(item.data)
            elif operation_type == "stop_bot":
                return self._handle_stop_bot(item.data)
            elif operation_type == "bot_status":
                return self._handle_bot_status(item.data)
            elif operation_type == "restart_bot":
                return self._handle_restart_bot(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            print(f"Error processing bot launcher queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_start_bot(self, data):
        """Handle bot start operations"""
        try:
            bot_type = data.get("type", "authoring")

            if bot_type == "authoring":
                from discord.authoring_bot import AuthoringBot

                self.bot_instance = AuthoringBot()
            elif bot_type == "character":
                from discord.character_system_bot import CharacterSystemBot

                self.bot_instance = CharacterSystemBot()
            else:
                return {"error": f"Unknown bot type: {bot_type}", "status": "failed"}

            # Start the bot
            self.bot_instance.start()
            return {
                "message": f"Bot {bot_type} started successfully",
                "status": "success",
            }
        except Exception as e:
            print(f"Error starting bot: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_stop_bot(self, data):
        """Handle bot stop operations"""
        try:
            if self.bot_instance:
                self.bot_instance.close()
                self.bot_instance = None
                return {"message": "Bot stopped successfully", "status": "success"}
            else:
                return {"message": "No bot running", "status": "success"}
        except Exception as e:
            print(f"Error stopping bot: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_bot_status(self, data):
        """Handle bot status queries"""
        try:
            if self.bot_instance:
                return {
                    "status": "running",
                    "bot_type": type(self.bot_instance).__name__,
                    "message": "Bot is currently running",
                }
            else:
                return {"status": "stopped", "message": "No bot is currently running"}
        except Exception as e:
            print(f"Error getting bot status: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_restart_bot(self, data):
        """Handle bot restart operations"""
        try:
            # Stop current bot
            stop_result = self._handle_stop_bot({})
            if stop_result.get("status") == "success":
                # Start new bot
                start_result = self._handle_start_bot(data)
                return {
                    "message": "Bot restarted successfully",
                    "stop_result": stop_result,
                    "start_result": start_result,
                    "status": "success",
                }
            else:
                return {"error": "Failed to stop current bot", "status": "failed"}
        except Exception as e:
            print(f"Error restarting bot: {e}")
            return {"error": str(e), "status": "failed"}


def main():
    """Main entry point for the bot"""
    print("🤖 Starting Foundry Bot with queue system...")

    try:
        # Create bot launcher with queue system
        launcher = BotLauncher()

        # Import and start the Discord bot
        from discord.authoring_bot import main as start_discord_bot

        start_discord_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
