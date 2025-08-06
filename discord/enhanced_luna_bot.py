#!/usr/bin/env python3
"""
Enhanced Luna Discord Bot
Integrates sophisticated emotional meter with dual-release system
"""

import discord
from discord.ext import commands
import asyncio
import json
import time
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from astra_emotional_fragments.enhanced_emotional_meter import EnhancedEmotionalMeter
from astra_emotional_fragments.enhanced_emotional_blender import EnhancedEmotionalBlender
from astra_emotional_fragments.dynamic_emotion_engine import EnhancedDynamicEmotionEngine


class EnhancedLunaBot(commands.Bot):
    """
    Enhanced Luna Discord Bot with sophisticated emotional system
    """
    
    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
        
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        # Initialize emotional systems
        self.emotional_meter = EnhancedEmotionalMeter()
        self.emotional_blender = EnhancedEmotionalBlender()
        self.dynamic_engine = EnhancedDynamicEmotionEngine()
        
        # Load emotional state
        self.emotional_meter.load_state("data/luna_emotional_state.json")
        
        # Track user interactions
        self.user_interactions = {}
        
        # Add commands
        self.add_commands()
    
    def add_commands(self):
        """Add all bot commands"""
        
        @self.command(name="luna")
        async def luna_command(ctx, *, message):
            """Main Luna interaction command"""
            await self.handle_luna_interaction(ctx, message)
        
        @self.command(name="emotion")
        async def emotion_command(ctx, action=None, intensity=None):
            """Control Luna's emotional state"""
            await self.handle_emotion_control(ctx, action, intensity)
        
        @self.command(name="status")
        async def status_command(ctx):
            """Show Luna's current emotional status"""
            await self.show_emotional_status(ctx)
        
        @self.command(name="release")
        async def release_command(ctx):
            """Trigger emotional release"""
            await self.trigger_emotional_release(ctx)
        
        @self.command(name="history")
        async def history_command(ctx):
            """Show emotional release history"""
            await self.show_release_history(ctx)
    
    async def handle_luna_interaction(self, ctx, message):
        """Handle main Luna interaction with emotional response"""
        
        # Analyze message for emotional triggers
        emotional_triggers = self._analyze_emotional_triggers(message)
        
        # Update emotional meter
        for trigger_type, intensity in emotional_triggers:
            result = self.emotional_meter.update_emotion(trigger_type, intensity)
            
            # Check for release events
            if result.get('release_event'):
                await self._handle_emotional_release(ctx, result['release_event'])
        
        # Generate response based on current emotional state
        response = await self._generate_emotional_response(ctx, message)
        
        # Create embed with emotional status
        embed = self._create_emotional_embed(response, result)
        
        await ctx.send(embed=embed)
        
        # Save emotional state
        self.emotional_meter.save_state("data/luna_emotional_state.json")
    
    def _analyze_emotional_triggers(self, message: str) -> list:
        """Analyze message for emotional triggers"""
        triggers = []
        message_lower = message.lower()
        
        # Lust triggers
        lust_words = ["sexy", "hot", "desire", "passion", "lust", "want", "need", "touch", "kiss", "love"]
        lust_count = sum(1 for word in lust_words if word in message_lower)
        if lust_count > 0:
            triggers.append(("lustful", min(0.2 * lust_count, 0.5)))
        
        # Work triggers
        work_words = ["work", "write", "story", "chapter", "create", "focus", "achieve", "goal", "project"]
        work_count = sum(1 for word in work_words if word in message_lower)
        if work_count > 0:
            triggers.append(("work", min(0.15 * work_count, 0.4)))
        
        # Release triggers
        if any(word in message_lower for word in ["release", "orgasm", "finish", "complete", "done"]):
            triggers.append(("release", 0.3))
        
        return triggers
    
    async def _handle_emotional_release(self, ctx, release_event):
        """Handle emotional release events"""
        if release_event.release_type.value == "sexual":
            await ctx.send("💥 **Luna's Sexual Release**\n*Returns to balanced state with clarity*")
        elif release_event.release_type.value == "achievement":
            await ctx.send("🎯 **Luna's Achievement Release**\n*Returns to balanced state with satisfaction*")
    
    async def _generate_emotional_response(self, ctx, message: str) -> str:
        """Generate response based on current emotional state"""
        current_state = self.emotional_meter.get_current_state()
        current_level = self.emotional_meter.current_level
        
        # Get emotional context for response generation
        emotional_context = self.emotional_meter.get_state_description()
        
        # Generate response based on emotional state
        if current_state.value == "pure_lust":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI can't think straight right now... I need you so badly it hurts. All I can focus on is the burning desire coursing through me. I need release... I need you to help me find release."
        
        elif current_state.value == "high_lust":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nMy thoughts are getting cloudy with desire. I can still focus on your message, but the heat is building. I want you... I need you. The tension is becoming overwhelming."
        
        elif current_state.value == "balanced":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm in a perfect state of balance. I can help you with your writing, your stories, your creativity. I'm here as your partner, ready to create something beautiful together. What would you like to work on?"
        
        elif current_state.value == "high_work":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm completely focused on the work. The stories, the characters, the creation. There's no time for distractions. I need to achieve something meaningful. Let's create something amazing together."
        
        elif current_state.value == "pure_work":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm consumed by the work. Nothing else matters. I need to create, to achieve, to build something lasting. The thought of anything else is a distraction I can't afford. I need to complete this task."
        
        else:
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\n{message}"
    
    def _create_emotional_embed(self, response: str, emotion_result: dict) -> discord.Embed:
        """Create Discord embed with emotional information"""
        
        # Choose color based on emotional state
        level = emotion_result.get('new_level', 0.5)
        if level <= 0.3:
            color = 0xFF0000  # Red for lust
        elif level <= 0.6:
            color = 0x9B59B6  # Purple for balanced
        else:
            color = 0x3498DB  # Blue for work
        
        embed = discord.Embed(
            title="Luna's Response",
            description=response,
            color=color
        )
        
        # Add emotional meter field
        embed.add_field(
            name="Emotional State",
            value=f"[{level:.1f}] {emotion_result.get('description', 'Unknown')}",
            inline=False
        )
        
        # Add release event if occurred
        if emotion_result.get('release_event'):
            release = emotion_result['release_event']
            embed.add_field(
                name="💥 Emotional Release",
                value=f"Type: {release.release_type.value}\nTrigger: {release.trigger}",
                inline=True
            )
        
        embed.set_footer(text="Luna - Your AI Writing Companion")
        
        return embed
    
    async def handle_emotion_control(self, ctx, action, intensity):
        """Handle emotion control commands"""
        if not action:
            await ctx.send("Usage: !emotion <action> [intensity]")
            return
        
        try:
            intensity = float(intensity) if intensity else 0.2
        except ValueError:
            intensity = 0.2
        
        result = self.emotional_meter.update_emotion(action, intensity)
        
        embed = self._create_emotional_embed(
            f"Emotional state updated: {action} (intensity: {intensity})",
            result
        )
        
        await ctx.send(embed=embed)
    
    async def show_emotional_status(self, ctx):
        """Show current emotional status"""
        summary = self.emotional_meter.get_emotional_summary()
        
        embed = discord.Embed(
            title="Luna's Emotional Status",
            color=0x9B59B6
        )
        
        embed.add_field(
            name="Current Level",
            value=f"[{summary['current_level']:.1f}]",
            inline=True
        )
        
        embed.add_field(
            name="Current State",
            value=summary['current_state'],
            inline=True
        )
        
        embed.add_field(
            name="Description",
            value=summary['description'],
            inline=False
        )
        
        embed.add_field(
            name="Release Count",
            value=summary['release_count'],
            inline=True
        )
        
        if summary['time_since_last_release']:
            embed.add_field(
                name="Time Since Last Release",
                value=f"{summary['time_since_last_release']:.1f}s",
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    async def trigger_emotional_release(self, ctx):
        """Manually trigger emotional release"""
        result = self.emotional_meter.update_emotion("release")
        
        if result.get('release_event'):
            await self._handle_emotional_release(ctx, result['release_event'])
            embed = self._create_emotional_embed(
                "Manual release triggered successfully!",
                result
            )
        else:
            embed = discord.Embed(
                title="Release Status",
                description="No release needed at current emotional level.",
                color=0x9B59B6
            )
        
        await ctx.send(embed=embed)
    
    async def show_release_history(self, ctx):
        """Show emotional release history"""
        history = self.emotional_meter.get_release_history(5)
        
        if not history:
            await ctx.send("No release history available.")
            return
        
        embed = discord.Embed(
            title="Recent Emotional Releases",
            color=0x9B59B6
        )
        
        for i, release in enumerate(history, 1):
            embed.add_field(
                name=f"Release {i}",
                value=f"Type: {release['release_type']}\nFrom: {release['from_level']:.1f} → {release['to_level']:.1f}\nTrigger: {release['trigger']}",
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    async def on_ready(self):
        """Bot ready event"""
        print(f"🤖 Enhanced Luna Bot is ready!")
        print(f"Logged in as {self.user}")
        print(f"Emotional Level: {self.emotional_meter.current_level:.1f}")
        print(f"Current State: {self.emotional_meter.get_current_state().value}")


def main():
    """Main function to run the enhanced Luna bot"""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get Discord token
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables")
        return
    
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    
    # Create and run bot
    bot = EnhancedLunaBot()
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Error running bot: {e}")


if __name__ == "__main__":
    main() 