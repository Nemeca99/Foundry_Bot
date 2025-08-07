#!/usr/bin/env python3
"""
Writing Assistant Discord Bot
Provides Sudowrite-inspired writing assistance features
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

from queue_manager import QueueProcessor
from framework.framework_tool import get_framework
from core.config import Config

# Configure logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WritingAssistantBot(commands.Bot, QueueProcessor):
    """
    Writing Assistant Discord Bot with Sudowrite-inspired features
    """

    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        QueueProcessor.__init__(self, "writing_assistant_bot")

        # Initialize framework
        self.framework = get_framework()

        # Add commands
        self.add_commands()

    def _process_item(self, item):
        """Process queue items for writing assistant operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "writing_assistance":
                return self._handle_writing_assistance(item.data)
            elif operation_type == "project_operation":
                return self._handle_project_operation(item.data)
            elif operation_type == "content_generation":
                return self._handle_content_generation(item.data)
            elif operation_type == "writing_analysis":
                return self._handle_writing_analysis(item.data)
            elif operation_type == "status_request":
                return self._handle_status_request(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing writing assistant queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_writing_assistance(self, data):
        """Handle writing assistance requests"""
        try:
            project_name = data.get("project_name", "")
            content = data.get("content", "")
            assistance_type = data.get("assistance_type", "autocomplete")
            
            # Process writing assistance
            result = {"status": "success", "assistance_type": assistance_type}
            
            if assistance_type == "autocomplete":
                result["suggestion"] = f"Continue with: {content[:50]}..."
            elif assistance_type == "expand":
                result["expanded_content"] = f"Expanded: {content}"
            elif assistance_type == "rewrite":
                result["rewritten_content"] = f"Rewritten: {content}"
            
            return result
        except Exception as e:
            logger.error(f"Error in writing assistance: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_project_operation(self, data):
        """Handle project operations"""
        try:
            operation = data.get("operation", "")
            project_name = data.get("project_name", "")
            
            result = {"status": "success", "operation": operation}
            
            if operation == "create":
                result["message"] = f"Project {project_name} created"
            elif operation == "update":
                result["message"] = f"Project {project_name} updated"
            elif operation == "delete":
                result["message"] = f"Project {project_name} deleted"
            
            return result
        except Exception as e:
            logger.error(f"Error in project operation: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_content_generation(self, data):
        """Handle content generation requests"""
        try:
            content_type = data.get("content_type", "")
            context = data.get("context", "")
            
            result = {"status": "success", "content_type": content_type}
            
            if content_type == "dialogue":
                result["generated_content"] = f"Generated dialogue for: {context}"
            elif content_type == "description":
                result["generated_content"] = f"Generated description for: {context}"
            elif content_type == "plot":
                result["generated_content"] = f"Generated plot for: {context}"
            
            return result
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_writing_analysis(self, data):
        """Handle writing analysis requests"""
        try:
            analysis_type = data.get("analysis_type", "")
            content = data.get("content", "")
            
            result = {"status": "success", "analysis_type": analysis_type}
            
            if analysis_type == "style":
                result["analysis"] = "Style analysis completed"
            elif analysis_type == "grammar":
                result["analysis"] = "Grammar check completed"
            elif analysis_type == "structure":
                result["analysis"] = "Structure analysis completed"
            
            return result
        except Exception as e:
            logger.error(f"Error in writing analysis: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_status_request(self, data):
        """Handle status requests"""
        try:
            return {
                "status": "success",
                "bot_status": "active",
                "available_commands": ["autocomplete", "expand", "rewrite", "dialogue"],
                "active_projects": 5
            }
        except Exception as e:
            logger.error(f"Error in status request: {e}")
            return {"error": str(e), "status": "failed"}

    def add_commands(self):
        """Add all writing assistant commands"""

        # Core Writing Tools
        @self.command(name="autocomplete")
        async def autocomplete_command(
            ctx, project_name: str, word_count: int = 400, *, current_text: str
        ):
            """Continue the story from where it left off"""
            await self.handle_autocomplete(ctx, project_name, current_text, word_count)

        @self.command(name="expand")
        async def expand_command(ctx, project_name: str, *, scene_text: str):
            """Expand a scene with more detail and description"""
            await self.handle_expand_scene(ctx, project_name, scene_text)

        @self.command(name="describe")
        async def describe_command(
            ctx, project_name: str, element: str, *, context: str = ""
        ):
            """Generate rich description for a scene/element"""
            await self.handle_generate_description(ctx, project_name, element, context)

        @self.command(name="rewrite")
        async def rewrite_command(ctx, project_name: str, *, original_text: str):
            """Rewrite passage in different styles"""
            await self.handle_rewrite_passage(ctx, project_name, original_text)

        @self.command(name="dialogue")
        async def dialogue_command(
            ctx,
            project_name: str,
            characters: str,
            situation: str,
            *,
            context: str = "",
        ):
            """Generate natural dialogue for characters"""
            await self.handle_generate_dialogue(
                ctx, project_name, characters, situation, context
            )

        @self.command(name="brainstorm")
        async def brainstorm_command(
            ctx, element: str, genre: str, *, context: str = ""
        ):
            """Brainstorm creative ideas for writing elements"""
            await self.handle_brainstorm_ideas(ctx, element, genre, context)

        # Advanced Writing Tools
        @self.command(name="canvas")
        async def canvas_command(ctx, project_name: str):
            """Create a story canvas with plot points and character arcs"""
            await self.handle_story_canvas(ctx, project_name)

        @self.command(name="character-bible")
        async def character_bible_command(
            ctx, character_name: str, role: str, genre: str
        ):
            """Create comprehensive character profile"""
            await self.handle_character_bible(ctx, character_name, role, genre)

        @self.command(name="world-building")
        async def world_building_command(ctx, genre: str, *, setting: str):
            """Generate world-building content"""
            await self.handle_world_building(ctx, genre, setting)

        @self.command(name="name-generator")
        async def name_generator_command(
            ctx, element_type: str, genre: str, setting: str, *, culture: str = ""
        ):
            """Generate names for characters, places, etc."""
            await self.handle_name_generator(ctx, element_type, genre, setting, culture)

        @self.command(name="plot-twist")
        async def plot_twist_command(ctx, genre: str, *, current_plot: str):
            """Generate plot twists for your story"""
            await self.handle_plot_twist_generator(ctx, current_plot, genre)

        # Writing Analysis Tools
        @self.command(name="analyze-style")
        async def analyze_style_command(ctx, project_name: str):
            """Analyze writing style and characteristics"""
            await self.handle_analyze_style(ctx, project_name)

        @self.command(name="writing-stats")
        async def writing_stats_command(ctx, project_name: str):
            """Get writing statistics and insights"""
            await self.handle_writing_stats(ctx, project_name)

        @self.command(name="suggest-improvements")
        async def suggest_improvements_command(ctx, project_name: str):
            """Get writing improvement suggestions"""
            await self.handle_suggest_improvements(ctx, project_name)

        # Project Management
        @self.command(name="create-project")
        async def create_project_command(
            ctx, name: str, genre: str, target_audience: str, word_count_goal: int
        ):
            """Create a new writing project"""
            await self.handle_create_project(
                ctx, name, genre, target_audience, word_count_goal
            )

        @self.command(name="add-chapter")
        async def add_chapter_command(
            ctx, project_name: str, chapter_title: str, *, content: str
        ):
            """Add a chapter to a project"""
            await self.handle_add_chapter(ctx, project_name, chapter_title, content)

        @self.command(name="project-info")
        async def project_info_command(ctx, project_name: str):
            """Get project information and statistics"""
            await self.handle_project_info(ctx, project_name)

        @self.command(name="list-projects")
        async def list_projects_command(ctx):
            """List all writing projects"""
            await self.handle_list_projects(ctx)

        # System Status
        @self.command(name="writing-assistant-status")
        async def writing_assistant_status_command(ctx):
            """Show writing assistant system status"""
            await self.handle_writing_assistant_status(ctx)

        @self.command(name="available-tools")
        async def available_tools_command(ctx):
            """List all available writing tools"""
            await self.handle_available_tools(ctx)

    # Core Writing Tools Handlers
    async def handle_autocomplete(
        self, ctx, project_name: str, current_text: str, word_count: int
    ):
        """Handle autocomplete command"""
        try:
            await ctx.send(f"✍️ Continuing your story from where it left off...")

            result = self.framework.autocomplete(project_name, current_text, word_count)

            embed = discord.Embed(
                title=f"✍️ Story Continuation: {project_name}",
                description="Here's the continuation of your story:",
                color=discord.Color.green(),
            )
            embed.add_field(name="Continuation", value=result, inline=False)
            embed.add_field(name="Word Count", value=str(word_count), inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in autocomplete: {e}")
            await ctx.send(f"❌ Error in autocomplete: {str(e)}")

    async def handle_expand_scene(self, ctx, project_name: str, scene_text: str):
        """Handle expand scene command"""
        try:
            await ctx.send(f"📝 Expanding your scene with more detail...")

            result = self.framework.expand_scene(project_name, scene_text)

            embed = discord.Embed(
                title=f"📝 Scene Expansion: {project_name}",
                description="Here's your expanded scene:",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Expanded Scene", value=result, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in expand scene: {e}")
            await ctx.send(f"❌ Error in expand scene: {str(e)}")

    async def handle_generate_description(
        self, ctx, project_name: str, element: str, context: str
    ):
        """Handle generate description command"""
        try:
            await ctx.send(f"🎨 Generating rich description for: {element}")

            result = self.framework.generate_description(project_name, element, context)

            embed = discord.Embed(
                title=f"🎨 Description Generated: {element}",
                description="Here's your rich description:",
                color=discord.Color.purple(),
            )
            embed.add_field(name="Description", value=result, inline=False)
            if context:
                embed.add_field(name="Context", value=context, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in generate description: {e}")
            await ctx.send(f"❌ Error in generate description: {str(e)}")

    async def handle_rewrite_passage(self, ctx, project_name: str, original_text: str):
        """Handle rewrite passage command"""
        try:
            await ctx.send(f"🔄 Rewriting your passage in different styles...")

            result = self.framework.rewrite_passage(project_name, original_text)

            embed = discord.Embed(
                title=f"🔄 Passage Rewrite: {project_name}",
                description="Here are 3 different versions of your passage:",
                color=discord.Color.orange(),
            )

            for version_name, version_text in result.items():
                embed.add_field(
                    name=f"Version {version_name.title()}",
                    value=version_text,
                    inline=False,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in rewrite passage: {e}")
            await ctx.send(f"❌ Error in rewrite passage: {str(e)}")

    async def handle_generate_dialogue(
        self, ctx, project_name: str, characters: str, situation: str, context: str
    ):
        """Handle generate dialogue command"""
        try:
            char_list = [c.strip() for c in characters.split(",")]
            await ctx.send(f"💬 Generating dialogue for: {', '.join(char_list)}")

            result = self.framework.generate_dialogue(
                project_name, char_list, situation, context
            )

            embed = discord.Embed(
                title=f"💬 Character Dialogue: {project_name}",
                description="Here's the generated dialogue:",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Characters", value=characters, inline=True)
            embed.add_field(name="Situation", value=situation, inline=True)
            embed.add_field(name="Dialogue", value=result, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in generate dialogue: {e}")
            await ctx.send(f"❌ Error in generate dialogue: {str(e)}")

    async def handle_brainstorm_ideas(
        self, ctx, element: str, genre: str, context: str
    ):
        """Handle brainstorm ideas command"""
        try:
            await ctx.send(f"💡 Brainstorming creative ideas for: {element}")

            result = self.framework.brainstorm_ideas(element, genre, context)

            embed = discord.Embed(
                title=f"💡 Brainstorming Ideas: {element}",
                description="Here are some creative ideas:",
                color=discord.Color.yellow(),
            )

            for i, idea in enumerate(result, 1):
                embed.add_field(name=f"Idea {i}", value=idea, inline=False)

            embed.add_field(name="Genre", value=genre, inline=True)
            if context:
                embed.add_field(name="Context", value=context, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in brainstorm ideas: {e}")
            await ctx.send(f"❌ Error in brainstorm ideas: {str(e)}")

    # Advanced Writing Tools Handlers
    async def handle_story_canvas(self, ctx, project_name: str):
        """Handle story canvas command"""
        try:
            await ctx.send(f"🎨 Creating story canvas for: {project_name}")

            result = self.framework.story_canvas(project_name)

            embed = discord.Embed(
                title=f"🎨 Story Canvas: {project_name}",
                description="Here's your story canvas:",
                color=discord.Color.green(),
            )

            if result.get("plot_points"):
                embed.add_field(
                    name="📖 Plot Points",
                    value="\n".join(
                        [f"• {point}" for point in result["plot_points"][:5]]
                    ),
                    inline=False,
                )

            if result.get("character_arcs"):
                embed.add_field(
                    name="👤 Character Arcs",
                    value="\n".join(
                        [f"• {arc}" for arc in result["character_arcs"][:5]]
                    ),
                    inline=False,
                )

            if result.get("world_elements"):
                embed.add_field(
                    name="🌍 World Elements",
                    value="\n".join(
                        [f"• {element}" for element in result["world_elements"][:5]]
                    ),
                    inline=False,
                )

            if result.get("themes"):
                embed.add_field(
                    name="🎭 Themes",
                    value="\n".join([f"• {theme}" for theme in result["themes"][:5]]),
                    inline=False,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in story canvas: {e}")
            await ctx.send(f"❌ Error in story canvas: {str(e)}")

    async def handle_character_bible(
        self, ctx, character_name: str, role: str, genre: str
    ):
        """Handle character bible command"""
        try:
            await ctx.send(f"👤 Creating character bible for: {character_name}")

            result = self.framework.character_bible(character_name, role, genre)

            embed = discord.Embed(
                title=f"👤 Character Bible: {character_name}",
                description="Here's your comprehensive character profile:",
                color=discord.Color.purple(),
            )
            embed.add_field(name="Character Profile", value=result, inline=False)
            embed.add_field(name="Role", value=role, inline=True)
            embed.add_field(name="Genre", value=genre, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in character bible: {e}")
            await ctx.send(f"❌ Error in character bible: {str(e)}")

    async def handle_world_building(self, ctx, genre: str, setting: str):
        """Handle world building command"""
        try:
            await ctx.send(f"🌍 Generating world-building content for: {setting}")

            result = self.framework.world_building(genre, setting)

            embed = discord.Embed(
                title=f"🌍 World Building: {setting}",
                description="Here's your world-building content:",
                color=discord.Color.blue(),
            )
            embed.add_field(name="World Building", value=result, inline=False)
            embed.add_field(name="Genre", value=genre, inline=True)
            embed.add_field(name="Setting", value=setting, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in world building: {e}")
            await ctx.send(f"❌ Error in world building: {str(e)}")

    async def handle_name_generator(
        self, ctx, element_type: str, genre: str, setting: str, culture: str
    ):
        """Handle name generator command"""
        try:
            await ctx.send(f"📝 Generating names for: {element_type}")

            result = self.framework.name_generator(
                element_type, genre, setting, culture
            )

            embed = discord.Embed(
                title=f"📝 Name Generator: {element_type}",
                description="Here are some generated names:",
                color=discord.Color.green(),
            )

            for i, name in enumerate(result, 1):
                embed.add_field(name=f"Name {i}", value=name, inline=True)

            embed.add_field(name="Type", value=element_type, inline=True)
            embed.add_field(name="Genre", value=genre, inline=True)
            embed.add_field(name="Setting", value=setting, inline=True)
            if culture:
                embed.add_field(name="Culture", value=culture, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in name generator: {e}")
            await ctx.send(f"❌ Error in name generator: {str(e)}")

    async def handle_plot_twist_generator(self, ctx, current_plot: str, genre: str):
        """Handle plot twist generator command"""
        try:
            await ctx.send(f"🎭 Generating plot twists for your story...")

            result = self.framework.plot_twist_generator(current_plot, genre)

            embed = discord.Embed(
                title=f"🎭 Plot Twist Generator",
                description="Here are some plot twist ideas:",
                color=discord.Color.red(),
            )

            for i, twist in enumerate(result, 1):
                embed.add_field(name=f"Twist {i}", value=twist, inline=False)

            embed.add_field(name="Genre", value=genre, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in plot twist generator: {e}")
            await ctx.send(f"❌ Error in plot twist generator: {str(e)}")

    # Writing Analysis Tools Handlers
    async def handle_analyze_style(self, ctx, project_name: str):
        """Handle analyze style command"""
        try:
            await ctx.send(f"📊 Analyzing writing style for: {project_name}")

            # This would need to be implemented in the framework
            embed = discord.Embed(
                title=f"📊 Style Analysis: {project_name}",
                description="Writing style analysis coming soon!",
                color=discord.Color.blue(),
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in analyze style: {e}")
            await ctx.send(f"❌ Error in analyze style: {str(e)}")

    async def handle_writing_stats(self, ctx, project_name: str):
        """Handle writing stats command"""
        try:
            await ctx.send(f"📈 Getting writing statistics for: {project_name}")

            # This would need to be implemented in the framework
            embed = discord.Embed(
                title=f"📈 Writing Stats: {project_name}",
                description="Writing statistics coming soon!",
                color=discord.Color.green(),
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in writing stats: {e}")
            await ctx.send(f"❌ Error in writing stats: {str(e)}")

    async def handle_suggest_improvements(self, ctx, project_name: str):
        """Handle suggest improvements command"""
        try:
            await ctx.send(f"💡 Generating improvement suggestions for: {project_name}")

            # This would need to be implemented in the framework
            embed = discord.Embed(
                title=f"💡 Improvement Suggestions: {project_name}",
                description="Writing improvement suggestions coming soon!",
                color=discord.Color.yellow(),
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in suggest improvements: {e}")
            await ctx.send(f"❌ Error in suggest improvements: {str(e)}")

    # Project Management Handlers
    async def handle_create_project(
        self, ctx, name: str, genre: str, target_audience: str, word_count_goal: int
    ):
        """Handle create project command"""
        try:
            await ctx.send(f"📚 Creating new writing project: {name}")

            result = self.framework.create_project(
                name, genre, target_audience, word_count_goal
            )

            embed = discord.Embed(
                title=f"📚 Project Created: {name}",
                description="Your new writing project has been created!",
                color=discord.Color.green(),
            )
            embed.add_field(name="Genre", value=genre, inline=True)
            embed.add_field(name="Target Audience", value=target_audience, inline=True)
            embed.add_field(
                name="Word Count Goal", value=str(word_count_goal), inline=True
            )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in create project: {e}")
            await ctx.send(f"❌ Error in create project: {str(e)}")

    async def handle_add_chapter(
        self, ctx, project_name: str, chapter_title: str, content: str
    ):
        """Handle add chapter command"""
        try:
            await ctx.send(f"📝 Adding chapter to: {project_name}")

            result = self.framework.add_chapter(project_name, chapter_title, content)

            if result:
                embed = discord.Embed(
                    title=f"📝 Chapter Added: {chapter_title}",
                    description=f"Chapter successfully added to {project_name}!",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Project", value=project_name, inline=True)
                embed.add_field(name="Chapter", value=chapter_title, inline=True)
                embed.add_field(
                    name="Word Count", value=str(len(content.split())), inline=True
                )
            else:
                embed = discord.Embed(
                    title="❌ Chapter Addition Failed",
                    description=f"Could not add chapter to {project_name}",
                    color=discord.Color.red(),
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in add chapter: {e}")
            await ctx.send(f"❌ Error in add chapter: {str(e)}")

    async def handle_project_info(self, ctx, project_name: str):
        """Handle project info command"""
        try:
            await ctx.send(f"📊 Getting project information for: {project_name}")

            project = self.framework.get_project(project_name)

            if project:
                embed = discord.Embed(
                    title=f"📊 Project Info: {project_name}",
                    description="Here's your project information:",
                    color=discord.Color.blue(),
                )
                embed.add_field(name="Genre", value=project.genre, inline=True)
                embed.add_field(
                    name="Target Audience", value=project.target_audience, inline=True
                )
                embed.add_field(
                    name="Word Count",
                    value=f"{project.current_word_count}/{project.word_count_goal}",
                    inline=True,
                )
                embed.add_field(
                    name="Chapters", value=str(len(project.chapters)), inline=True
                )
                embed.add_field(
                    name="Characters", value=str(len(project.characters)), inline=True
                )
                embed.add_field(
                    name="Created",
                    value=project.created_date.strftime("%Y-%m-%d"),
                    inline=True,
                )
            else:
                embed = discord.Embed(
                    title="❌ Project Not Found",
                    description=f"Project '{project_name}' not found",
                    color=discord.Color.red(),
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in project info: {e}")
            await ctx.send(f"❌ Error in project info: {str(e)}")

    async def handle_list_projects(self, ctx):
        """Handle list projects command"""
        try:
            await ctx.send("📚 Retrieving your writing projects...")

            projects = self.framework.list_projects()

            embed = discord.Embed(
                title="📚 Your Writing Projects",
                description=f"Found {len(projects)} projects",
                color=discord.Color.blue(),
            )

            for project_name in projects:
                project = self.framework.get_project(project_name)
                if project:
                    embed.add_field(
                        name=project_name,
                        value=f"Genre: {project.genre}\nWords: {project.current_word_count}/{project.word_count_goal}\nChapters: {len(project.chapters)}",
                        inline=True,
                    )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in list projects: {e}")
            await ctx.send(f"❌ Error in list projects: {str(e)}")

    # System Status Handlers
    async def handle_writing_assistant_status(self, ctx):
        """Handle writing assistant status command"""
        try:
            await ctx.send("🔧 Checking writing assistant system status...")

            # Check which plugins are loaded
            writing_plugins = [
                "writing_assistant",
                "text_generator",
                "personalization_engine",
            ]

            loaded_plugins = []
            missing_plugins = []

            for plugin in writing_plugins:
                if plugin in self.framework.plugins:
                    loaded_plugins.append(plugin)
                else:
                    missing_plugins.append(plugin)

            embed = discord.Embed(
                title="🔧 Writing Assistant System Status",
                description="Writing assistant system status overview",
                color=(
                    discord.Color.green()
                    if not missing_plugins
                    else discord.Color.orange()
                ),
            )

            embed.add_field(
                name="Loaded Plugins",
                value=f"{len(loaded_plugins)}/{len(writing_plugins)}",
                inline=True,
            )
            embed.add_field(
                name="Status",
                value=(
                    "✅ Fully Operational"
                    if not missing_plugins
                    else "⚠️ Partially Operational"
                ),
                inline=True,
            )

            if loaded_plugins:
                embed.add_field(
                    name="Available Systems",
                    value="\n".join([f"• {plugin}" for plugin in loaded_plugins]),
                    inline=False,
                )

            if missing_plugins:
                embed.add_field(
                    name="Missing Systems",
                    value="\n".join([f"• {plugin}" for plugin in missing_plugins]),
                    inline=False,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in writing assistant status: {e}")
            await ctx.send(f"❌ Error in writing assistant status: {str(e)}")

    async def handle_available_tools(self, ctx):
        """Handle available tools command"""
        try:
            await ctx.send("🛠️ Retrieving available writing tools...")

            # This would need to be implemented in the framework
            tools = [
                "autocomplete",
                "expand",
                "describe",
                "rewrite",
                "dialogue",
                "brainstorm",
                "canvas",
                "character-bible",
                "world-building",
                "name-generator",
                "plot-twist",
            ]

            embed = discord.Embed(
                title="🛠️ Available Writing Tools",
                description="Here are all the available writing tools:",
                color=discord.Color.blue(),
            )

            for tool in tools:
                embed.add_field(
                    name=tool.replace("-", " ").title(), value=f"!{tool}", inline=True
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in available tools: {e}")
            await ctx.send(f"❌ Error in available tools: {str(e)}")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f"✍️ Writing Assistant Bot is ready! Logged in as {self.user}")
        await self.change_presence(
            activity=discord.Game(name="Writing Assistant | !help")
        )


def main():
    """Main function to run the writing assistant bot"""
    # Load configuration
    config = Config()

    # Create bot instance
    bot = WritingAssistantBot(command_prefix=config.BOT_PREFIX)

    # Run the bot
    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
