#!/usr/bin/env python3
"""
Enhanced Luna Discord Bot
Provides sophisticated emotional system integration
"""

import discord
from discord.ext import commands
import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add framework to path
framework_dir = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_dir))

# Add astra_emotional_fragments to path
astra_dir = Path(__file__).parent.parent / "astra_emotional_fragments"
sys.path.insert(0, str(astra_dir))

from queue_manager import QueueProcessor
from enhanced_emotional_meter import EnhancedEmotionalMeter
from emotional_blender import EnhancedEmotionalBlender
from dynamic_emotion_engine import (
    EnhancedDynamicEmotionEngine,
)


class EnhancedLunaBot(commands.Bot, QueueProcessor):
    """
    Enhanced Luna Discord Bot with sophisticated emotional system
    """

    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        QueueProcessor.__init__(self, "enhanced_luna_bot")

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

        @self.command(name="weights")
        async def weights_command(ctx, *, message=None):
            """Show weight analysis for a message"""
            await self.show_weight_analysis(ctx, message)

        @self.command(name="release")
        async def release_command(ctx):
            """Trigger emotional release"""
            await self.trigger_emotional_release(ctx)

        @self.command(name="history")
        async def history_command(ctx):
            """Show emotional release history"""
            await self.show_release_history(ctx)

        @self.command(name="reset")
        async def reset_command(ctx):
            """Reset Luna's emotional state to balanced"""
            await self.reset_emotional_state(ctx)

        @self.command(name="build")
        async def build_command(ctx, emotion_type: str):
            """Build up Luna's emotional state"""
            await self.build_emotional_state(ctx, emotion_type)

        # Simulacra Game Commands
        @self.command(name="simulacra")
        async def simulacra_command(ctx, action: str, *, params: str = ""):
            """Main Simulacra game command"""
            await self.handle_simulacra_command(ctx, action, params)

        @self.command(name="hatch")
        async def hatch_command(ctx, drone_type: str = "standard", *, name: str = ""):
            """Hatch a new Simulacra drone"""
            await self.hatch_simulacra_drone(ctx, drone_type, name)

        @self.command(name="simulate")
        async def simulate_command(ctx, duration: int = 60, drone_count: int = 10):
            """Simulate the Simulacra world"""
            await self.simulate_simulacra_world(ctx, duration, drone_count)

        @self.command(name="gacha")
        async def gacha_command(ctx, amount: int = 1):
            """Perform a gacha pull"""
            await self.simulacra_gacha_pull(ctx, amount)

        @self.command(name="drone")
        async def drone_command(ctx, *, drone_name: str):
            """Get information about a Simulacra drone"""
            await self.get_simulacra_drone_info(ctx, drone_name)

        @self.command(name="kingdom")
        async def kingdom_command(ctx, action: str, *, params: str = ""):
            """Manage Simulacra kingdoms"""
            await self.manage_simulacra_kingdom(ctx, action, params)

        @self.command(name="resources")
        async def resources_command(ctx, action: str, *, params: str = ""):
            """Manage Simulacra resources"""
            await self.manage_simulacra_resources(ctx, action, params)

        @self.command(name="hunt")
        async def hunt_command(ctx, action: str, *, params: str = ""):
            """Manage Simulacra hunting"""
            await self.manage_simulacra_hunting(ctx, action, params)

        @self.command(name="trade")
        async def trade_command(ctx, action: str, *, params: str = ""):
            """Manage Simulacra trading"""
            await self.manage_simulacra_trade(ctx, action, params)

        @self.command(name="leaderboard")
        async def leaderboard_command(ctx):
            """Show Simulacra leaderboard"""
            await self.show_simulacra_leaderboard(ctx)

        @self.command(name="disasters")
        async def disasters_command(ctx):
            """Show active Simulacra disasters"""
            await self.show_simulacra_disasters(ctx)

        @self.command(name="network")
        async def network_command(ctx):
            """Show Simulacra network consciousness state"""
            await self.show_simulacra_network_state(ctx)

        # Luna NPC Integration Commands
        @self.command(name="embody")
        async def embody_command(ctx, npc_type: str):
            """Embody a Luna emotional fragment as an NPC"""
            await self.embody_luna_npc(ctx, npc_type)

        @self.command(name="talk")
        async def talk_command(ctx, npc_type: str, *, message: str):
            """Talk to an embodied Luna NPC"""
            await self.talk_to_luna_npc(ctx, npc_type, message)

        @self.command(name="npcs")
        async def npcs_command(ctx):
            """Show currently active Luna NPCs"""
            await self.show_active_luna_npcs(ctx)

        @self.command(name="release_npc")
        async def release_npc_command(ctx, npc_type: str):
            """Release an embodied Luna NPC"""
            await self.release_luna_npc(ctx, npc_type)

        @self.command(name="memories")
        async def memories_command(ctx, npc_type: str):
            """Show memories of interactions with a Luna NPC"""
            await self.show_npc_memories(ctx, npc_type)

    async def handle_luna_interaction(self, ctx_or_message, message_text):
        """Handle main Luna interaction with emotional response using global weight system"""

        # Determine if this is a context or message object
        if hasattr(ctx_or_message, "send"):
            # It's a context object
            ctx = ctx_or_message
            message = message_text
        else:
            # It's a message object
            message = ctx_or_message
            ctx = message.channel
            message = message_text

        # Use the new global weight calculation system
        result = self.emotional_meter.update_emotion_with_global_weight(message)

        # Check for release events
        if result.get("release_event"):
            await self._handle_emotional_release(ctx, result["release_event"])

        # Generate LLM response with emotional context
        llm_response = await self._generate_llm_response(ctx, message, result)

        # Create embed with detailed emotional information
        embed = self._create_detailed_emotional_embed(llm_response, result)

        await ctx.send(embed=embed)

        # Save emotional state
        self.emotional_meter.save_state("data/luna_emotional_state.json")

    async def _generate_llm_response(
        self, ctx, message: str, emotion_result: dict
    ) -> str:
        """Generate LLM response with emotional context"""
        try:
            # Get current emotional state
            current_state = self.emotional_meter.get_current_state()
            current_level = self.emotional_meter.current_level

            # Create emotional context for the LLM
            emotional_context = f"""
Current Emotional State: {current_state.value} (Level: {current_level:.3f})
Emotional Description: {emotion_result.get('description', 'Unknown')}

You are Luna, an AI writing companion with emotional intelligence. Respond to the user's message while reflecting your current emotional state.
"""

            # Use the framework's text generation
            from framework.framework_tool import get_framework

            framework = get_framework()

            # Create the prompt with emotional context
            prompt = f"{emotional_context}\n\nUser: {message}\n\nLuna:"

            # Generate response using the framework's text generator (synchronous)
            llm_response = framework.generate_text(prompt)

            if llm_response:
                return llm_response
            else:
                return "I'm having trouble thinking clearly right now... Let me try to focus on helping you with your writing."

        except Exception as e:
            return f"I'm experiencing some technical difficulties... (Error: {str(e)})"

    def _analyze_emotional_triggers(self, message: str) -> list:
        """Analyze message for emotional triggers"""
        triggers = []
        message_lower = message.lower()

        # Lust triggers
        lust_words = [
            "sexy",
            "hot",
            "desire",
            "passion",
            "lust",
            "want",
            "need",
            "touch",
            "kiss",
            "love",
        ]
        lust_count = sum(1 for word in lust_words if word in message_lower)
        if lust_count > 0:
            triggers.append(("lustful", min(0.2 * lust_count, 0.5)))

        # Work triggers
        work_words = [
            "work",
            "write",
            "story",
            "chapter",
            "create",
            "focus",
            "achieve",
            "goal",
            "project",
        ]
        work_count = sum(1 for word in work_words if word in message_lower)
        if work_count > 0:
            triggers.append(("work", min(0.15 * work_count, 0.4)))

        # Release triggers
        if any(
            word in message_lower
            for word in ["release", "orgasm", "finish", "complete", "done"]
        ):
            triggers.append(("release", 0.3))

        return triggers

    async def _handle_emotional_release(self, ctx, release_event):
        """Handle emotional release events"""
        if release_event.release_type.value == "sexual":
            await ctx.send(
                "💥 **Luna's Sexual Release**\n*Returns to balanced state with clarity*"
            )
        elif release_event.release_type.value == "achievement":
            await ctx.send(
                "🎯 **Luna's Achievement Release**\n*Returns to balanced state with satisfaction*"
            )

    async def _generate_emotional_response(
        self, ctx, message: str, emotion_result: dict
    ) -> str:
        """Generate response based on current emotional state with global weight context"""
        current_state = self.emotional_meter.get_current_state()
        current_level = self.emotional_meter.current_level

        # Get weight calculations
        weight_calc = emotion_result.get("global_weight_calculation", {})
        lust_avg = weight_calc.get("lust_average", 0)
        work_avg = weight_calc.get("work_average", 0)
        weight_diff = weight_calc.get("weight_difference", 0)

        # Generate response based on emotional state
        if current_state.value == "pure_lust":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI can't think straight right now... I need you so badly it hurts. All I can focus on is the burning desire coursing through me. I need release... I need you to help me find release."

        elif current_state.value == "high_lust":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nMy thoughts are getting cloudy with desire. I can still focus on your message, but the heat is building. I want you... I need you. The tension is becoming overwhelming."

        elif current_state.value == "moderate_lust":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI'm feeling a bit distracted by desire, but I can still help you with your writing. Though the thought of you is making it hard to concentrate..."

        elif current_state.value == "balanced":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI'm in a perfect state of balance. I can help you with your writing, your stories, your creativity. I'm here as your partner, ready to create something beautiful together. What would you like to work on?"

        elif current_state.value == "moderate_work":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI'm focused on the work, but I can still appreciate other things. Let's create something amazing together."

        elif current_state.value == "high_work":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI'm completely focused on the work. The stories, the characters, the creation. There's no time for distractions. I need to achieve something meaningful. Let's create something amazing together."

        elif current_state.value == "pure_work":
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\nI'm consumed by the work. Nothing else matters. I need to create, to achieve, to build something lasting. The thought of anything else is a distraction I can't afford. I need to complete this task."

        else:
            return f"*[EMOTIONAL METER: {current_level:.3f}]*\n\n{message}"

    def _create_detailed_emotional_embed(
        self, response: str, emotion_result: dict
    ) -> discord.Embed:
        """Create Discord embed with detailed emotional information"""

        # Choose color based on emotional state
        level = emotion_result.get("new_level", 0.5)
        if level <= 0.3:
            color = 0xFF0000  # Red for lust
        elif level <= 0.6:
            color = 0x9B59B6  # Purple for balanced
        else:
            color = 0x3498DB  # Blue for work

        embed = discord.Embed(
            title="Luna's Response", description=response, color=color
        )

        # Add emotional meter field
        embed.add_field(
            name="Emotional State",
            value=f"[{level:.3f}] {emotion_result.get('description', 'Unknown')}",
            inline=False,
        )

        # Add weight calculations
        weight_calc = emotion_result.get("global_weight_calculation", {})
        if weight_calc:
            lust_avg = weight_calc.get("lust_average", 0)
            work_avg = weight_calc.get("work_average", 0)
            weight_diff = weight_calc.get("weight_difference", 0)

            embed.add_field(
                name="Weight Analysis",
                value=f"Lust: {lust_avg:.3f}\nWork: {work_avg:.3f}\nDifference: {weight_diff:.3f}",
                inline=True,
            )

        # Add release event if occurred
        if emotion_result.get("release_event"):
            release = emotion_result["release_event"]
            embed.add_field(
                name="💥 Emotional Release",
                value=f"Type: {release.release_type.value}\nTrigger: {release.trigger}\nFrom: {release.from_level:.3f} → {release.to_level:.3f}",
                inline=True,
            )

        embed.set_footer(
            text="Luna - Your AI Writing Companion with Global Emotional Intelligence"
        )

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
            f"Emotional state updated: {action} (intensity: {intensity})", result
        )

        await ctx.send(embed=embed)

    async def show_emotional_status(self, ctx):
        """Show current emotional status"""
        summary = self.emotional_meter.get_emotional_summary()

        embed = discord.Embed(title="Luna's Emotional Status", color=0x9B59B6)

        embed.add_field(
            name="Current Level", value=f"[{summary['current_level']:.1f}]", inline=True
        )

        embed.add_field(
            name="Current State", value=summary["current_state"], inline=True
        )

        embed.add_field(name="Description", value=summary["description"], inline=False)

        embed.add_field(
            name="Release Count", value=summary["release_count"], inline=True
        )

        if summary["time_since_last_release"]:
            embed.add_field(
                name="Time Since Last Release",
                value=f"{summary['time_since_last_release']:.1f}s",
                inline=True,
            )

        await ctx.send(embed=embed)

    async def trigger_emotional_release(self, ctx):
        """Manually trigger emotional release"""
        result = self.emotional_meter.update_emotion("release")

        if result.get("release_event"):
            await self._handle_emotional_release(ctx, result["release_event"])
            embed = self._create_emotional_embed(
                "Manual release triggered successfully!", result
            )
        else:
            embed = discord.Embed(
                title="Release Status",
                description="No release needed at current emotional level.",
                color=0x9B59B6,
            )

        await ctx.send(embed=embed)

    async def show_release_history(self, ctx):
        """Show emotional release history"""
        history = self.emotional_meter.get_release_history(5)

        if not history:
            await ctx.send("No release history available.")
            return

        embed = discord.Embed(title="Recent Emotional Releases", color=0x9B59B6)

        for i, release in enumerate(history, 1):
            embed.add_field(
                name=f"Release {i}",
                value=f"Type: {release['release_type']}\nFrom: {release['from_level']:.1f} → {release['to_level']:.1f}\nTrigger: {release['trigger']}",
                inline=True,
            )

        await ctx.send(embed=embed)

    async def on_ready(self):
        """Bot ready event"""
        print(f"🤖 Enhanced Luna Bot is ready!")
        print(f"Logged in as {self.user}")
        print(f"Emotional Level: {self.emotional_meter.current_level:.1f}")
        print(f"Current State: {self.emotional_meter.get_current_state().value}")

    async def on_message(self, message):
        """Handle all messages"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Process commands first
        await self.process_commands(message)

        # If it's not a command, treat it as a Luna interaction
        if not message.content.startswith("!"):
            await self.handle_luna_interaction(message, message.content)

    async def show_weight_analysis(self, ctx, message):
        """Show detailed weight analysis for a message"""
        if not message:
            await ctx.send("Usage: !weights <message>")
            return

        # Calculate weights without updating emotional state
        lust_avg = self.emotional_meter._calculate_lust_average(message)
        work_avg = self.emotional_meter._calculate_work_average(message)
        weight_diff = self.emotional_meter._calculate_weight_difference(message)

        # Create embed
        embed = discord.Embed(
            title="Weight Analysis",
            description=f"Analysis for: '{message}'",
            color=0x9B59B6,
        )

        embed.add_field(
            name="Lust Analysis",
            value=f"Average: {lust_avg:.3f}\nWords: {self._get_lust_words(message)}",
            inline=True,
        )

        embed.add_field(
            name="Work Analysis",
            value=f"Average: {work_avg:.3f}\nWords: {self._get_work_words(message)}",
            inline=True,
        )

        embed.add_field(
            name="Weight Difference",
            value=f"{weight_diff:.3f} ({'Work' if weight_diff > 0 else 'Lust' if weight_diff < 0 else 'Balanced'} bias)",
            inline=False,
        )

        await ctx.send(embed=embed)

    def _get_lust_words(self, message: str) -> str:
        """Get lust words found in message"""
        message_lower = message.lower()
        found_words = [
            word
            for word in self.emotional_meter.lust_weights.keys()
            if word in message_lower
        ]
        return ", ".join(found_words) if found_words else "None"

    def _get_work_words(self, message: str) -> str:
        """Get work words found in message"""
        message_lower = message.lower()
        found_words = [
            word
            for word in self.emotional_meter.work_weights.keys()
            if word in message_lower
        ]
        return ", ".join(found_words) if found_words else "None"

    async def reset_emotional_state(self, ctx):
        """Reset Luna's emotional state to balanced"""
        self.emotional_meter.current_level = 0.5
        self.emotional_meter.save_state("data/luna_emotional_state.json")

        embed = discord.Embed(
            title="Emotional State Reset",
            description="Luna's emotional state has been reset to balanced (0.500)",
            color=0x9B59B6,
        )

        await ctx.send(embed=embed)

    async def build_emotional_state(self, ctx, emotion_type: str):
        """Build up Luna's emotional state"""
        emotion_type = emotion_type.lower()

        if emotion_type in ["lust", "sexy", "desire"]:
            # Build up lust
            messages = [
                "You're so beautiful and sexy",
                "I want you so badly",
                "I need to touch you and kiss you",
                "I can't think of anything but your body",
                "I need you now, I want you",
            ]

            embed = discord.Embed(
                title="Building Lust",
                description="Building up Luna's lust...",
                color=0xFF0000,
            )

            await ctx.send(embed=embed)

            for message in messages:
                result = self.emotional_meter.update_emotion_with_global_weight(message)
                await ctx.send(f"`{message}` → Level: {result['new_level']:.3f}")
                await asyncio.sleep(1)

        elif emotion_type in ["work", "focus", "achieve"]:
            # Build up work focus
            messages = [
                "I need to work on my story",
                "I must achieve my goals",
                "I need to create a masterpiece",
                "I must focus on excellence",
                "I need to complete this project",
            ]

            embed = discord.Embed(
                title="Building Work Focus",
                description="Building up Luna's work focus...",
                color=0x3498DB,
            )

            await ctx.send(embed=embed)

            for message in messages:
                result = self.emotional_meter.update_emotion_with_global_weight(message)
                await ctx.send(f"`{message}` → Level: {result['new_level']:.3f}")
                await asyncio.sleep(1)

        else:
            await ctx.send("Usage: !build <lust|work>")
            return

        # Show final state
        status = self.emotional_meter.get_emotional_summary()
        final_embed = discord.Embed(
            title="Build Complete",
            description=f"Final Level: {status['current_level']:.3f} - {status['current_state']}",
            color=0x9B59B6,
        )

        await ctx.send(embed=final_embed)

    # Simulacra Game Command Handlers
    async def handle_simulacra_command(self, ctx, action: str, params: str):
        """Handle main Simulacra game command"""
        try:
            # Import framework
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            if action == "status":
                result = await framework.get_simulacra_game_status(user_id)
                await self._send_simulacra_result(ctx, "Game Status", result)

            elif action == "help":
                await self._send_simulacra_help(ctx)

            else:
                await ctx.send(
                    f"❌ Unknown Simulacra action: {action}. Use `!simulacra help` for available commands."
                )

        except Exception as e:
            await ctx.send(f"❌ Error in Simulacra command: {str(e)}")

    async def hatch_simulacra_drone(self, ctx, drone_type: str, name: str):
        """Hatch a new Simulacra drone"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)
            drone_name = name if name else None

            result = await framework.hatch_simulacra_drone(
                user_id, drone_type, drone_name
            )
            await self._send_simulacra_result(ctx, "Drone Hatching", result)

        except Exception as e:
            await ctx.send(f"❌ Error hatching drone: {str(e)}")

    async def simulate_simulacra_world(self, ctx, duration: int, drone_count: int):
        """Simulate the Simulacra world"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            await ctx.send(
                f"🌍 Starting world simulation for {duration} seconds with {drone_count} drones..."
            )

            result = await framework.simulate_simulacra_world(duration, drone_count)
            await self._send_simulacra_result(ctx, "World Simulation", result)

        except Exception as e:
            await ctx.send(f"❌ Error simulating world: {str(e)}")

    async def simulacra_gacha_pull(self, ctx, amount: int):
        """Perform a gacha pull"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            result = await framework.simulacra_gacha_pull(user_id, amount)
            await self._send_simulacra_result(ctx, "Gacha Pull", result)

        except Exception as e:
            await ctx.send(f"❌ Error in gacha pull: {str(e)}")

    async def get_simulacra_drone_info(self, ctx, drone_name: str):
        """Get information about a Simulacra drone"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_simulacra_drone_info(drone_name)
            await self._send_simulacra_result(ctx, "Drone Information", result)

        except Exception as e:
            await ctx.send(f"❌ Error getting drone info: {str(e)}")

    async def manage_simulacra_kingdom(self, ctx, action: str, params: str):
        """Manage Simulacra kingdoms"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            # Parse parameters
            kwargs = {}
            if params:
                for param in params.split():
                    if "=" in param:
                        key, value = param.split("=", 1)
                        kwargs[key] = value

            result = await framework.manage_simulacra_kingdom(user_id, action, **kwargs)
            await self._send_simulacra_result(ctx, f"Kingdom {action.title()}", result)

        except Exception as e:
            await ctx.send(f"❌ Error in kingdom management: {str(e)}")

    async def manage_simulacra_resources(self, ctx, action: str, params: str):
        """Manage Simulacra resources"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            # Parse parameters
            kwargs = {}
            if params:
                for param in params.split():
                    if "=" in param:
                        key, value = param.split("=", 1)
                        kwargs[key] = value

            result = await framework.manage_simulacra_resources(
                user_id, action, **kwargs
            )
            await self._send_simulacra_result(ctx, f"Resource {action.title()}", result)

        except Exception as e:
            await ctx.send(f"❌ Error in resource management: {str(e)}")

    async def manage_simulacra_hunting(self, ctx, action: str, params: str):
        """Manage Simulacra hunting"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            # Parse parameters
            kwargs = {}
            if params:
                for param in params.split():
                    if "=" in param:
                        key, value = param.split("=", 1)
                        kwargs[key] = value

            result = await framework.manage_simulacra_hunting(user_id, action, **kwargs)
            await self._send_simulacra_result(ctx, f"Hunting {action.title()}", result)

        except Exception as e:
            await ctx.send(f"❌ Error in hunting management: {str(e)}")

    async def manage_simulacra_trade(self, ctx, action: str, params: str):
        """Manage Simulacra trading"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            user_id = str(ctx.author.id)

            # Parse parameters
            kwargs = {}
            if params:
                for param in params.split():
                    if "=" in param:
                        key, value = param.split("=", 1)
                        kwargs[key] = value

            result = await framework.manage_simulacra_trade(user_id, action, **kwargs)
            await self._send_simulacra_result(ctx, f"Trade {action.title()}", result)

        except Exception as e:
            await ctx.send(f"❌ Error in trade management: {str(e)}")

    async def show_simulacra_leaderboard(self, ctx):
        """Show Simulacra leaderboard"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_simulacra_leaderboard()
            await self._send_simulacra_result(ctx, "Leaderboard", result)

        except Exception as e:
            await ctx.send(f"❌ Error getting leaderboard: {str(e)}")

    async def show_simulacra_disasters(self, ctx):
        """Show active Simulacra disasters"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_simulacra_disasters()
            await self._send_simulacra_result(ctx, "Active Disasters", result)

        except Exception as e:
            await ctx.send(f"❌ Error getting disasters: {str(e)}")

    async def show_simulacra_network_state(self, ctx):
        """Show Simulacra network consciousness state"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_simulacra_network_state()
            await self._send_simulacra_result(ctx, "Network Consciousness", result)

        except Exception as e:
            await ctx.send(f"❌ Error getting network state: {str(e)}")

    async def _send_simulacra_result(self, ctx, title: str, result: dict):
        """Send Simulacra command result as embed"""
        embed = discord.Embed(
            title=f"🎮 {title}",
            color=0x00FF00 if result.get("success", False) else 0xFF0000,
            timestamp=discord.utils.utcnow(),
        )

        if result.get("success", False):
            embed.description = result.get(
                "message", "Operation completed successfully"
            )

            # Add fields based on result type
            if "drone" in result:
                drone = result["drone"]
                embed.add_field(
                    name="🤖 Drone Name",
                    value=drone.get("name", "Unknown"),
                    inline=True,
                )
                embed.add_field(
                    name="🔧 Drone Type",
                    value=drone.get("type", "Unknown"),
                    inline=True,
                )
                embed.add_field(
                    name="🆔 Drone ID", value=drone.get("id", "Unknown"), inline=True
                )

            if "pulls" in result:
                pulls = result["pulls"]
                embed.add_field(name="🎰 Pulls", value=str(len(pulls)), inline=True)
                embed.add_field(
                    name="💰 Cost", value=f"{result.get('cost', 0)} RP", inline=True
                )

                for i, pull in enumerate(pulls[:5]):  # Show first 5 pulls
                    embed.add_field(
                        name=f"📦 Pull {i+1}",
                        value=f"{pull.get('name', 'Unknown')} ({pull.get('rarity', 'Unknown')})",
                        inline=True,
                    )

            if "leaderboard" in result:
                leaderboard = result["leaderboard"]
                embed.add_field(
                    name="🏆 Top Players", value=str(len(leaderboard)), inline=True
                )

                for i, entry in enumerate(leaderboard[:5]):  # Show top 5
                    embed.add_field(
                        name=f"#{i+1}",
                        value=f"{entry.get('name', 'Unknown')} - {entry.get('score', 0)}",
                        inline=True,
                    )

            if "disasters" in result:
                disasters = result["disasters"]
                embed.add_field(
                    name="🌪️ Active Disasters", value=str(len(disasters)), inline=True
                )

                for disaster in disasters[:3]:  # Show first 3
                    embed.add_field(
                        name="⚠️ Disaster",
                        value=f"{disaster.get('type', 'Unknown')} - {disaster.get('severity', 'Unknown')}",
                        inline=True,
                    )

            if "network_state" in result:
                network = result["network_state"]
                embed.add_field(
                    name="🧠 Network Status",
                    value=network.get("status", "Unknown"),
                    inline=True,
                )
                embed.add_field(
                    name="🔗 Connections",
                    value=str(network.get("connections", 0)),
                    inline=True,
                )
                embed.add_field(
                    name="💭 Consciousness Level",
                    value=str(network.get("consciousness_level", 0)),
                    inline=True,
                )

        else:
            embed.description = result.get("error", "Operation failed")

        await ctx.send(embed=embed)

    # Luna NPC Integration Handlers
    async def embody_luna_npc(self, ctx, npc_type: str):
        """Embody a Luna emotional fragment as an NPC"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()
            user_id = str(ctx.author.id)

            result = await framework.embody_luna_npc(npc_type, user_id)

            if result.get("success"):
                embed = discord.Embed(
                    title=f"🎭 {result['npc']['name']} Embodied!",
                    description=result["message"],
                    color=0x00FF00,
                )
                embed.add_field(name="Role", value=result["npc"]["role"], inline=True)
                embed.add_field(
                    name="Personality", value=result["npc"]["personality"], inline=True
                )
                embed.add_field(
                    name="Abilities", value=", ".join(result["abilities"]), inline=False
                )
                embed.set_footer(text=f"Embody time: {result['npc']['embodied_at']}")
            else:
                embed = discord.Embed(
                    title="❌ Embodiment Failed",
                    description=result.get("error", "Unknown error"),
                    color=0xFF0000,
                )
                if "available_npcs" in result:
                    embed.add_field(
                        name="Available NPCs",
                        value=", ".join(result["available_npcs"]),
                        inline=False,
                    )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error embodying NPC: {str(e)}")

    async def talk_to_luna_npc(self, ctx, npc_type: str, message: str):
        """Talk to an embodied Luna NPC"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()
            user_id = str(ctx.author.id)

            result = await framework.interact_with_luna_npc(npc_type, message, user_id)

            if result.get("success"):
                embed = discord.Embed(
                    title=f"{result['npc_emoji']} {result['npc_name']}",
                    description=result["response"],
                    color=0x0099FF,
                )
                embed.add_field(name="Role", value=result["role"], inline=True)
                embed.add_field(
                    name="Personality", value=result["personality"], inline=True
                )
                embed.set_footer(text=f"User: {ctx.author.display_name}")
            else:
                embed = discord.Embed(
                    title="❌ Interaction Failed",
                    description=result.get("error", "Unknown error"),
                    color=0xFF0000,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error talking to NPC: {str(e)}")

    async def show_active_luna_npcs(self, ctx):
        """Show currently active Luna NPCs"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_active_luna_npcs()

            if result.get("success"):
                embed = discord.Embed(
                    title="🎭 Active Luna NPCs",
                    description=f"Currently embodied: {result['total_active']}",
                    color=0x0099FF,
                )

                if result["active_npcs"]:
                    for npc in result["active_npcs"]:
                        embed.add_field(
                            name=f"{npc['emoji']} {npc['name']}",
                            value=f"Role: {npc['role']}\nEmbodied: {npc['embodied_at']}",
                            inline=True,
                        )
                else:
                    embed.add_field(
                        name="No Active NPCs",
                        value="No Luna NPCs are currently embodied.",
                        inline=False,
                    )

                embed.add_field(
                    name="Available NPCs",
                    value=", ".join(result["available_npcs"]),
                    inline=False,
                )
            else:
                embed = discord.Embed(
                    title="❌ Failed to Get NPCs",
                    description=result.get("error", "Unknown error"),
                    color=0xFF0000,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error getting active NPCs: {str(e)}")

    async def release_luna_npc(self, ctx, npc_type: str):
        """Release an embodied Luna NPC"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.release_luna_npc(npc_type)

            if result.get("success"):
                embed = discord.Embed(
                    title="🎭 NPC Released",
                    description=result["message"],
                    color=0x00FF00,
                )
                embed.add_field(
                    name="Released At", value=result["released_at"], inline=True
                )
            else:
                embed = discord.Embed(
                    title="❌ Release Failed",
                    description=result.get("error", "Unknown error"),
                    color=0xFF0000,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error releasing NPC: {str(e)}")

    async def show_npc_memories(self, ctx, npc_type: str):
        """Show memories of interactions with a Luna NPC"""
        try:
            from framework.framework_tool import get_framework

            framework = get_framework()

            result = await framework.get_npc_memories(npc_type)

            if result.get("success"):
                embed = discord.Embed(
                    title=f"🧠 {npc_type.title()} Memories",
                    description=f"Total memories: {result['total_memories']}",
                    color=0x0099FF,
                )

                if result["memories"]:
                    # Show last 5 memories
                    recent_memories = result["memories"][-5:]
                    for i, memory in enumerate(recent_memories):
                        embed.add_field(
                            name=f"Memory {i+1}",
                            value=f"User: {memory.get('user_id', 'Unknown')}\nMessage: {memory.get('message', 'N/A')}\nResponse: {memory.get('response', 'N/A')}",
                            inline=False,
                        )
                else:
                    embed.add_field(
                        name="No Memories",
                        value="No interactions recorded yet.",
                        inline=False,
                    )
            else:
                embed = discord.Embed(
                    title="❌ Failed to Get Memories",
                    description=result.get("error", "Unknown error"),
                    color=0xFF0000,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error getting NPC memories: {str(e)}")

    async def _send_simulacra_help(self, ctx):
        """Send Simulacra help information"""
        embed = discord.Embed(
            title="🎮 Simulacra Rancher Commands",
            description="Available commands for the Simulacra game system",
            color=0x0099FF,
        )

        commands = [
            ("!simulacra status", "Get your current game status"),
            ("!hatch [type] [name]", "Hatch a new drone"),
            ("!simulate [duration] [drones]", "Simulate the world"),
            ("!gacha [amount]", "Perform gacha pulls"),
            ("!drone [name]", "Get drone information"),
            ("!kingdom [action] [params]", "Manage kingdoms"),
            ("!resources [action] [params]", "Manage resources"),
            ("!hunt [action] [params]", "Manage hunting"),
            ("!trade [action] [params]", "Manage trading"),
            ("!leaderboard", "Show leaderboard"),
            ("!disasters", "Show active disasters"),
            ("!network", "Show network consciousness"),
            ("!embody [npc_type]", "Embody a Luna emotional fragment as NPC"),
            ("!talk [npc_type] [message]", "Talk to an embodied Luna NPC"),
            ("!npcs", "Show currently active Luna NPCs"),
            ("!release [npc_type]", "Release an embodied Luna NPC"),
            ("!memories [npc_type]", "Show NPC interaction memories"),
        ]

        for cmd, desc in commands:
            embed.add_field(name=cmd, value=desc, inline=False)

        await ctx.send(embed=embed)


def main():
    """Main function to run the enhanced Luna bot"""
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Get Discord token
    token = os.getenv("DISCORD_TOKEN")
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
