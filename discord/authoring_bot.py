"""
BULMA HEADER PROTOCOL - DISCORD/AUTHORING_BOT.PY
=================================================

FILE IDENTITY:
- Name: Authoring Bot Discord Interface
- Role: Discord bot interface for authoring capabilities
- Purpose: Provides Discord commands for text, image, video, and voice generation
- Location: discord/authoring_bot.py (Discord bot interface)

BULMA USAGE PATTERNS:
- READ FIRST: This file handles all Discord interactions for authoring
- MODIFICATIONS: Changes here affect Discord command functionality
- TESTING: Test all Discord commands after modifications
- INTEGRATION: Coordinates with framework and plugins

KEY COMPONENTS:
1. AuthoringBot - Main Discord bot class
2. Command handlers for all authoring capabilities
3. Project management commands
4. Media generation commands
5. Business tracking commands
6. Error handling and logging

BULMA RESTRICTIONS:
- DO NOT modify command structure without testing Discord integration
- DO NOT change permission handling without security review
- ALWAYS test commands with proper error handling
- CHECK that all authoring capabilities work through Discord
- VERIFY user permissions and channel restrictions

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This file is the primary interface for authoring bot functionality.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import framework
from framework.framework_tool import get_framework

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AuthoringBot:
    """Discord bot for authoring capabilities"""

    def __init__(self):
        self.framework = get_framework()
        self.config = self.framework.config

        # Initialize Discord bot
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        self.bot = commands.Bot(
            command_prefix=self.config["bot_prefix"], intents=intents, help_command=None
        )

        # Set up command handlers
        self._setup_commands()

        logger.info("✅ Authoring Bot initialized")

    def _setup_commands(self):
        """Set up all Discord commands"""

        @self.bot.event
        async def on_ready():
            """Bot ready event"""
            logger.info(f"🤖 Authoring Bot logged in as {self.bot.user}")
            await self.bot.change_presence(
                activity=discord.Game(name="Authoring Assistant")
            )

        @self.bot.event
        async def on_message(ctx):
            """Handle all messages including @mentions"""
            # Don't respond to our own messages
            if ctx.author == self.bot.user:
                return

            # Check if bot is mentioned
            if self.bot.user.mentioned_in(ctx):
                # Remove the mention and get the actual message
                message_content = (
                    ctx.content.replace(f"<@{self.bot.user.id}>", "")
                    .replace(f"<@!{self.bot.user.id}>", "")
                    .strip()
                )

                if not message_content:
                    # Just a mention, give a friendly response
                    response = "🌟 Hello! I'm Luna, your AI writing partner! I'm here to help you create amazing content. Try `!help` to see all the things I can do for you!"
                    await ctx.send(response)
                    return

                # Process the message as a natural language request
                try:
                    # Use the tools command functionality for natural language
                    result = await self._handle_natural_language(ctx, message_content)
                    await self._send_long_message(
                        ctx.channel, result, "🤖 Luna's Response:"
                    )
                except Exception as e:
                    await ctx.channel.send(
                        f"❌ Sorry, I encountered an error: {str(e)}"
                    )
                return

            # Process commands normally
            await self.bot.process_commands(ctx)

        @self.bot.event
        async def on_command_error(ctx, error):
            """Handle command errors"""
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(
                    "❌ Command not found. Use `!help` for available commands."
                )
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send("❌ You don't have permission to use this command.")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send(f"❌ An error occurred: {str(error)}")

        @self.bot.command(name="help")
        async def help_command(ctx):
            """Show help information"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            help_text = """🌟 **LUNA - Your AI Writing Partner**

**Quick Start:**
- Just @mention me for natural conversation!
- `!help` - See all commands
- `!create-project "Name" "Genre" "Audience" word_count` - Start a project

**Writing Assistant:**
`!autocomplete <project> <text>` - Continue your story
`!expand <project> <scene>` - Add detail to scenes
`!describe <project> <element> <context>` - Generate descriptions
`!rewrite <project> <text>` - Create multiple versions
`!dialogue <project> <characters> <situation>` - Generate dialogue
`!brainstorm <element> <genre> <context>` - Creative ideas

**Project Management:**
`!create-project <name> <genre> <audience> <word_count>`
`!list-projects` - Show all projects
`!write-chapter <project> <title> <requirements>` - Write chapters

**AI Tools:**
`!tools <your request>` - Natural language requests
Examples: `!tools Create a fantasy character` or `!tools Write a chapter about dragons`

**Personalization:**
`!personalize analyze` - Analyze your writing style
`!personality show` - See Luna's personality
`!personality-test <type>` - Start personality test (writing_style, communication_style, learning_preferences)
`!learning-summary` - Show Luna's learning progress
`!modify-message <type> <message>` - Modify message for better understanding
            `!reward-learning <activity> <level>` - Reward Luna for learning (testing)
            `!punish-learning <opportunity> <severity>` - Punish Luna for missed learning (testing)
            `!test-emotion <message>` - Test dynamic emotion adaptation
            `!blend-emotions <primary> [secondary] [tertiary]` - Blend multiple emotions
            `!test-prompt-injection <message>` - Test prompt injection system

**Multimodal Generation:**
`!generate-multimodal <prompt> [media_types] [style]` - Generate text, image, voice, video, audio
`!create-character-media <name> <description> [media_types]` - Create character multimedia
`!create-story-media <title> <genre> [media_types]` - Create story multimedia
`!generate-image <prompt> [style]` - Generate image with Stable Diffusion
`!generate-voice <text> [style]` - Generate voice from text
`!generate-video <prompt> [duration]` - Generate video from prompt
`!generate-sound <prompt> [style]` - Generate sound effects

**Example:** `!create-project "My Novel" "Fantasy" "Young Adult" 50000`
"""
            await self._send_long_message(ctx, help_text, "📚 **LUNA COMMANDS**")

        @self.bot.command(name="create-project")
        async def create_project(ctx, *, args: str = ""):
            """Create a new authoring project"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments from the string
                if not args:
                    await ctx.send(
                        '❌ Please provide project details. Example: `!create-project "My Novel" "Fantasy" "Young Adult" 50000`'
                    )
                    return

                # Split the arguments, handling quoted strings
                import shlex

                try:
                    parsed_args = shlex.split(args)
                    if len(parsed_args) < 4:
                        await ctx.send(
                            '❌ Please provide: name, genre, audience, and word count. Example: `!create-project "My Novel" "Fantasy" "Young Adult" 50000`'
                        )
                        return

                    name = parsed_args[0]
                    genre = parsed_args[1]
                    audience = parsed_args[2]
                    word_count = int(parsed_args[3])

                    project = self.framework.create_project(
                        name, genre, audience, word_count
                    )
                    await ctx.send(
                        f"✅ Created project '{name}':\n- Genre: {genre}\n- Audience: {audience}\n- Word Count Goal: {word_count:,}"
                    )
                except ValueError:
                    await ctx.send(
                        '❌ Word count must be a number. Example: `!create-project "My Novel" "Fantasy" "Young Adult" 50000`'
                    )
                except Exception as e:
                    await ctx.send(f"❌ Failed to create project: {str(e)}")
            except Exception as e:
                await ctx.send(f"❌ Failed to create project: {str(e)}")

        @self.bot.command(name="list-projects")
        async def list_projects(ctx):
            """List all projects"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            projects = self.framework.list_projects()
            if not projects:
                await ctx.send(
                    "📚 No projects found. Create one with `!create-project`"
                )
                return

            project_list = "📚 **Your Projects:**\n"
            for name in projects:
                project = self.framework.get_project(name)
                project_list += f"- **{name}** ({project.genre}, {project.current_word_count:,}/{project.word_count_goal:,} words)\n"

            await ctx.send(project_list)

        @self.bot.command(name="project-info")
        async def project_info(ctx, name: str):
            """Show detailed project information"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            project = self.framework.get_project(name)
            if not project:
                await ctx.send(f"❌ Project '{name}' not found")
                return

            info = f"""📖 **Project: {name}**

**Details:**
- Genre: {project.genre}
- Target Audience: {project.target_audience}
- Word Count: {project.current_word_count:,}/{project.word_count_goal:,} ({project.current_word_count/project.word_count_goal*100:.1f}%)
- Chapters: {len(project.chapters)}
- Characters: {len(project.characters)}
- Created: {project.created_date.strftime('%Y-%m-%d')}
- Last Modified: {project.last_modified.strftime('%Y-%m-%d %H:%M')}

**Recent Activity:**
"""

            if project.chapters:
                recent_chapters = project.chapters[-3:]
                info += "Recent Chapters:\n"
                for chapter in recent_chapters:
                    info += f"- Chapter {chapter['chapter_number']}: {chapter['title']} ({chapter['word_count']} words)\n"

            if project.characters:
                info += f"\nCharacters: {', '.join([c['name'] for c in project.characters])}"

            await ctx.send(info)

        @self.bot.command(name="write-chapter")
        async def write_chapter(
            ctx, project_name: str, chapter_title: str, *, requirements: str
        ):
            """Write a chapter for a project"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(
                f"📝 Writing chapter '{chapter_title}' for project '{project_name}'..."
            )

            try:
                if "text_generator" in self.framework.plugins:
                    result = self.framework.plugins["text_generator"].write_chapter(
                        project_name, chapter_title, requirements
                    )

                    # Use the helper method for long messages
                    await self._send_long_message(ctx, result)
                else:
                    await ctx.send("❌ Text generation plugin not available")

            except Exception as e:
                await ctx.send(f"❌ Failed to write chapter: {str(e)}")

        @self.bot.command(name="develop-character")
        async def develop_character(
            ctx, project_name: str, character_name: str, *, requirements: str
        ):
            """Develop a character for a project"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(
                f"👤 Developing character '{character_name}' for project '{project_name}'..."
            )

            try:
                if "text_generator" in self.framework.plugins:
                    result = self.framework.plugins["text_generator"].develop_character(
                        project_name, character_name, requirements
                    )

                    # Use the helper method for long messages
                    await self._send_long_message(ctx, result)
                else:
                    await ctx.send("❌ Text generation plugin not available")

            except Exception as e:
                await ctx.send(f"❌ Failed to develop character: {str(e)}")

        @self.bot.command(name="generate-plot")
        async def generate_plot(ctx, project_name: str, *, requirements: str):
            """Generate a plot outline for a project"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(
                f"📋 Generating plot outline for project '{project_name}'..."
            )

            try:
                if "text_generator" in self.framework.plugins:
                    result = self.framework.plugins["text_generator"].generate_plot(
                        project_name, requirements
                    )

                    # Use the helper method for long messages
                    await self._send_long_message(ctx, result)
                else:
                    await ctx.send("❌ Text generation plugin not available")

            except Exception as e:
                await ctx.send(f"❌ Failed to generate plot: {str(e)}")

        @self.bot.command(name="write-story")
        async def write_story(ctx, genre: str, audience: str, *, requirements: str):
            """Write a complete story"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(f"📖 Writing {genre} story for {audience} audience...")

            try:
                if "text_generator" in self.framework.plugins:
                    result = self.framework.plugins["text_generator"].write_story(
                        genre, audience, requirements
                    )

                    # Use the helper method for long messages
                    await self._send_long_message(ctx, result)
                else:
                    await ctx.send("❌ Text generation plugin not available")

            except Exception as e:
                await ctx.send(f"❌ Failed to write story: {str(e)}")

        @self.bot.command(name="generate-cover")
        async def generate_cover(ctx, project_name: str, *, description: str):
            """Generate a book cover"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(f"🎨 Generating book cover for '{project_name}'...")

            try:
                result = self.framework.generate_image(description, "book_cover")
                await ctx.send(f"✅ Cover generated: {result}")
            except Exception as e:
                await ctx.send(f"❌ Failed to generate cover: {str(e)}")

        @self.bot.command(name="create-trailer")
        async def create_trailer(ctx, project_name: str, *, description: str):
            """Generate a book trailer"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(f"🎬 Creating book trailer for '{project_name}'...")

            try:
                result = self.framework.generate_video(description, 30)
                await ctx.send(f"✅ Trailer created: {result}")
            except Exception as e:
                await ctx.send(f"❌ Failed to create trailer: {str(e)}")

        @self.bot.command(name="narrate-chapter")
        async def narrate_chapter(ctx, project_name: str, chapter_number: int):
            """Create audiobook narration for a chapter"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            await ctx.send(
                f"🎤 Narrating chapter {chapter_number} of '{project_name}'..."
            )

            try:
                project = self.framework.get_project(project_name)
                if not project:
                    await ctx.send(f"❌ Project '{project_name}' not found")
                    return

                if chapter_number < 1 or chapter_number > len(project.chapters):
                    await ctx.send(f"❌ Chapter {chapter_number} not found")
                    return

                chapter = project.chapters[chapter_number - 1]
                result = self.framework.generate_voice(chapter["content"], "narrator")
                await ctx.send(f"✅ Narration created: {result}")
            except Exception as e:
                await ctx.send(f"❌ Failed to narrate chapter: {str(e)}")

        @self.bot.command(name="track-sales")
        async def track_sales(ctx, project_name: str, revenue: float, royalties: float):
            """Track sales data for a project"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                sales_data = {
                    "revenue": revenue,
                    "royalties": royalties,
                    "date": datetime.now().isoformat(),
                }

                if self.framework.track_sales(project_name, sales_data):
                    await ctx.send(
                        f"💰 Updated sales data for '{project_name}':\n- Revenue: ${revenue:,.2f}\n- Royalties: ${royalties:,.2f}"
                    )
                else:
                    await ctx.send(f"❌ Failed to track sales for '{project_name}'")
            except Exception as e:
                await ctx.send(f"❌ Failed to track sales: {str(e)}")

        @self.bot.command(name="get-stats")
        async def get_stats(ctx):
            """Show authoring statistics"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                stats = self.framework.get_stats()

                stats_text = f"""📊 **Authoring Statistics**

**Overall Progress:**
- Total Words Written: {stats['total_words_written']:,}
- Total Chapters Completed: {stats['total_chapters_completed']}
- Total Characters Created: {stats['total_characters_created']}
- Total Projects: {stats['total_projects']}

**Financial:**
- Total Sales: ${stats['total_sales']:,.2f}
- Total Royalties: ${stats['total_royalties']:,.2f}

**Writing Streak:**
- Current Streak: {stats['writing_streak_days']} days
- Average Words per Session: {stats['average_words_per_session']:.0f}

**Projects:**
"""

                for name, project_stats in stats["projects"].items():
                    progress = (
                        project_stats["word_count"] / project_stats["goal"]
                    ) * 100
                    stats_text += f"- **{name}**: {progress:.1f}% complete ({project_stats['word_count']:,}/{project_stats['goal']:,} words)\n"

                await ctx.send(stats_text)
            except Exception as e:
                await ctx.send(f"❌ Failed to get stats: {str(e)}")

        @self.bot.command(name="learning-stats")
        async def learning_stats(ctx):
            """Show learning engine statistics"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                if "learning_engine" not in self.framework.plugins:
                    await ctx.send("❌ Learning Engine plugin not available.")
                    return

                learning_engine = self.framework.plugins["learning_engine"]
                stats = learning_engine.get_learning_stats()

                stats_text = f"""🧠 **Learning Statistics**

**Processing Progress:**
- Total Chunks Processed: {stats['total_chunks_processed']:,}
- Total Words Processed: {stats['total_words_processed']:,}
- Wikipedia Chunks: {stats['wikipedia_chunks']:,}
- Book Chunks: {stats['book_chunks']:,}
- Processing Errors: {stats['processing_errors_count']}

**Last Processed:** {stats['last_processed_date'] or 'Never'}
**Output Directory:** {stats['output_directory']}
"""
                await ctx.send(stats_text)
            except Exception as e:
                await ctx.send(f"❌ Failed to get learning stats: {str(e)}")

        @self.bot.command(name="personalize")
        async def personalize_command(
            ctx, action: str = "analyze", *, details: str = ""
        ):
            """Personalization commands for writing style analysis"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                personalization_engine = self.framework.get_plugin(
                    "personalization_engine"
                )
                if not personalization_engine:
                    await ctx.send("❌ Personalization engine not available")
                    return

                if action.lower() == "analyze":
                    # Send initial response
                    embed = discord.Embed(
                        title="🔍 Analyzing Your Writing Style",
                        description="Processing your Book_Collection to understand your writing style...",
                        color=0x0099FF,
                        timestamp=datetime.now(),
                    )
                    status_msg = await ctx.send(embed=embed)

                    # Analyze writing style
                    style_data = personalization_engine.analyze_writing_style()

                    embed = discord.Embed(
                        title="✅ Writing Style Analysis Complete",
                        color=0x00FF00,
                        timestamp=datetime.now(),
                    )

                    characteristics = style_data.get("characteristics", {})
                    embed.add_field(
                        name="📊 Writing Characteristics",
                        value=f"Avg Sentence Length: {characteristics.get('avg_sentence_length', 0):.1f} words\n"
                        f"Total Words Analyzed: {characteristics.get('total_words_analyzed', 0):,}\n"
                        f"Vocabulary Richness: {characteristics.get('vocabulary_richness', 0):.2f}",
                        inline=True,
                    )

                    vocabulary = style_data.get("vocabulary", {})
                    if vocabulary:
                        top_words = list(vocabulary.keys())[:5]
                        embed.add_field(
                            name="📝 Common Words",
                            value=", ".join(top_words),
                            inline=True,
                        )

                    await status_msg.edit(embed=embed)

                elif action.lower() == "suggestions":
                    suggestions = personalization_engine.get_writing_suggestions()

                    embed = discord.Embed(
                        title="💡 Personalized Writing Suggestions",
                        color=0x0099FF,
                        timestamp=datetime.now(),
                    )

                    if suggestions["style_recommendations"]:
                        embed.add_field(
                            name="🎨 Style Recommendations",
                            value="\n".join(suggestions["style_recommendations"]),
                            inline=False,
                        )

                    if suggestions["vocabulary_suggestions"]:
                        embed.add_field(
                            name="📚 Vocabulary Suggestions",
                            value="\n".join(suggestions["vocabulary_suggestions"][:5]),
                            inline=False,
                        )

                    if suggestions["thematic_elements"]:
                        embed.add_field(
                            name="🎭 Thematic Elements",
                            value="\n".join(suggestions["thematic_elements"][:5]),
                            inline=False,
                        )

                    await ctx.send(embed=embed)

                elif action.lower() == "stats":
                    stats = personalization_engine.get_personalization_stats()

                    embed = discord.Embed(
                        title="📈 Personalization Statistics",
                        color=0x0099FF,
                        timestamp=datetime.now(),
                    )

                    embed.add_field(
                        name="🔍 Analysis Status",
                        value=f"Writing Fingerprint: {'✅' if stats['writing_fingerprint_analyzed'] else '❌'}\n"
                        f"Conversation History: {stats['conversation_history_count']} interactions\n"
                        f"Style Preferences: {stats['style_preferences_count']} saved",
                        inline=True,
                    )

                    embed.add_field(
                        name="📊 Writing Stats",
                        value=f"Words Analyzed: {stats['total_words_analyzed']:,}\n"
                        f"Avg Sentence Length: {stats['avg_sentence_length']:.1f} words",
                        inline=True,
                    )

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(
                        "❌ Unknown action. Use: `analyze`, `suggestions`, or `stats`"
                    )

            except Exception as e:
                logger.error(f"❌ Error in personalize command: {e}")
                await ctx.send(f"❌ Error: {str(e)}")

        @self.bot.command(name="tools")
        async def tools_command(ctx, *, message: str):
            """Use AI tools for enhanced authoring capabilities"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Send initial response
                embed = discord.Embed(
                    title="🔧 AI Tools Processing",
                    description="Processing your request with AI tools...",
                    color=0x0099FF,
                    timestamp=datetime.now(),
                )
                status_msg = await ctx.send(embed=embed)

                # Call the framework with tool use
                result = self.framework.call_with_tools(message)

                if "error" in result:
                    embed = discord.Embed(
                        title="❌ Tool Use Error",
                        description=result["error"],
                        color=0xFF0000,
                        timestamp=datetime.now(),
                    )
                    await status_msg.edit(embed=embed)
                    return

                # Create response embed
                if result.get("type") == "tool_response":
                    embed = discord.Embed(
                        title="✅ AI Tools Response",
                        description=result["content"],
                        color=0x00FF00,
                        timestamp=datetime.now(),
                    )

                    # Add tool results if available
                    if "tool_results" in result:
                        tool_info = []
                        for tool_result in result["tool_results"]:
                            tool_info.append(
                                f"**{tool_result['function_name']}**: {tool_result['result'].get('message', 'Executed')}"
                            )

                        if tool_info:
                            embed.add_field(
                                name="🔧 Tools Used",
                                value="\n".join(tool_info),
                                inline=False,
                            )
                else:
                    embed = discord.Embed(
                        title="💬 AI Response",
                        description=result.get("content", "No response generated"),
                        color=0x0099FF,
                        timestamp=datetime.now(),
                    )

                # Split long messages
                if len(embed.description) > 2000:
                    chunks = self._split_message(embed.description, 1900)
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            embed.description = chunk
                            await status_msg.edit(embed=embed)
                        else:
                            await ctx.send(chunk)
                else:
                    await status_msg.edit(embed=embed)

            except Exception as e:
                logger.error(f"❌ Error in tools command: {e}")
                await ctx.send(f"❌ Error: {str(e)}")

        @self.bot.command(name="status")
        async def status(ctx):
            """Show bot status"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            status_text = f"""🤖 **Authoring Bot Status**

**Bot Info:**
- Status: Online
- Framework: Loaded
- Plugins: {len(self.framework.plugins)} loaded

**Available Plugins:**
"""

            for plugin_name in self.framework.plugins.keys():
                status_text += f"- {plugin_name}\n"

            await ctx.send(status_text)

        # Writing Assistant Commands (Sudowrite-inspired)
        @self.bot.command(name="autocomplete")
        async def autocomplete(ctx, project_name: str, *, current_text: str):
            """Continue the story from where it left off (like Sudowrite's Write feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🖊️ Generating continuation...")
                continuation = writing_assistant.autocomplete(
                    project_name, current_text
                )

                await self._send_long_message(
                    ctx, continuation, "📝 **Story Continuation:**"
                )

            except Exception as e:
                logger.error(f"❌ Error with autocomplete: {e}")
                await ctx.send(f"❌ Error generating continuation: {e}")

        @self.bot.command(name="expand")
        async def expand_scene(ctx, project_name: str, *, scene_text: str):
            """Expand a rushed scene with more detail (like Sudowrite's Expand feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("📝 Expanding scene...")
                expanded = writing_assistant.expand_scene(project_name, scene_text)

                await self._send_long_message(ctx, expanded, "📖 **Expanded Scene:**")

            except Exception as e:
                logger.error(f"❌ Error expanding scene: {e}")
                await ctx.send(f"❌ Error expanding scene: {e}")

        @self.bot.command(name="describe")
        async def describe_element(
            ctx, project_name: str, element: str, *, context: str = ""
        ):
            """Generate rich descriptions (like Sudowrite's Describe feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🎨 Generating description...")
                description = writing_assistant.generate_description(
                    project_name, element, context
                )

                await self._send_long_message(
                    ctx, description, f"🎨 **Description of {element}:**"
                )

            except Exception as e:
                logger.error(f"❌ Error generating description: {e}")
                await ctx.send(f"❌ Error generating description: {e}")

        @self.bot.command(name="rewrite")
        async def rewrite_passage(ctx, project_name: str, *, original_text: str):
            """Generate multiple versions of a passage (like Sudowrite's Rewrite feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("✏️ Rewriting passage...")
                versions = writing_assistant.rewrite_passage(
                    project_name, original_text
                )

                if "error" in versions:
                    await ctx.send(f"❌ {versions['error']}")
                    return

                # Send each version
                for style, text in versions.items():
                    if text:
                        await self._send_long_message(
                            ctx,
                            text,
                            f"✏️ **{style.replace('_', ' ').title()} Version:**",
                        )

            except Exception as e:
                logger.error(f"❌ Error rewriting passage: {e}")
                await ctx.send(f"❌ Error rewriting passage: {e}")

        @self.bot.command(name="dialogue")
        async def generate_dialogue(
            ctx,
            project_name: str,
            characters: str,
            situation: str,
            *,
            context: str = "",
        ):
            """Generate character dialogue"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                char_list = [c.strip() for c in characters.split(",")]

                await ctx.send("💬 Generating dialogue...")
                dialogue = writing_assistant.generate_dialogue(
                    project_name, char_list, situation, context
                )

                await self._send_long_message(
                    ctx, dialogue, "💬 **Character Dialogue:**"
                )

            except Exception as e:
                logger.error(f"❌ Error generating dialogue: {e}")
                await ctx.send(f"❌ Error generating dialogue: {e}")

        @self.bot.command(name="brainstorm")
        async def brainstorm_ideas(ctx, element: str, genre: str, *, context: str = ""):
            """Brainstorm creative ideas (like Sudowrite's Brainstorm feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("💡 Brainstorming ideas...")
                ideas = writing_assistant.brainstorm_ideas(element, genre, context)

                if ideas:
                    ideas_text = "\n".join([f"• {idea}" for idea in ideas])
                    await self._send_long_message(
                        ctx, ideas_text, "💡 **Brainstormed Ideas:**"
                    )
                else:
                    await ctx.send("❌ No ideas generated")

            except Exception as e:
                logger.error(f"❌ Error brainstorming: {e}")
                await ctx.send(f"❌ Error brainstorming ideas: {e}")

        @self.bot.command(name="canvas")
        async def story_canvas(ctx, project_name: str):
            """Create a story canvas with plot points and character arcs (like Sudowrite's Canvas feature)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🎨 Creating story canvas...")
                canvas = writing_assistant.story_canvas(project_name)

                if "error" in canvas:
                    await ctx.send(f"❌ {canvas['error']}")
                    return

                # Create embed for canvas
                embed = discord.Embed(
                    title=f"🎨 Story Canvas: {project_name}",
                    description="Plot points and character arcs",
                    color=0x9B59B6,
                )

                if canvas.get("plot_points"):
                    embed.add_field(
                        name="📖 Plot Points",
                        value="\n".join(
                            [f"• {point}" for point in canvas["plot_points"][:5]]
                        ),
                        inline=False,
                    )

                if canvas.get("character_arcs"):
                    embed.add_field(
                        name="👤 Character Arcs",
                        value="\n".join(
                            [f"• {arc}" for arc in canvas["character_arcs"][:5]]
                        ),
                        inline=False,
                    )

                await ctx.send(embed=embed)

            except Exception as e:
                logger.error(f"❌ Error creating canvas: {e}")
                await ctx.send(f"❌ Error creating story canvas: {e}")

        @self.bot.command(name="character-bible")
        async def character_bible(ctx, character_name: str, role: str, genre: str):
            """Create comprehensive character profile (like Sudowrite's character development)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("👤 Creating character bible...")
                profile = writing_assistant.character_bible(character_name, role, genre)

                await self._send_long_message(
                    ctx, profile, f"👤 **Character Bible: {character_name}**"
                )

            except Exception as e:
                logger.error(f"❌ Error creating character bible: {e}")
                await ctx.send(f"❌ Error creating character bible: {e}")

        @self.bot.command(name="world-building")
        async def world_building(ctx, genre: str, setting: str):
            """Generate world-building elements"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🌍 Creating world-building...")
                world = writing_assistant.world_building(genre, setting)

                await self._send_long_message(ctx, world, "🌍 **World-Building:**")

            except Exception as e:
                logger.error(f"❌ Error creating world-building: {e}")
                await ctx.send(f"❌ Error creating world-building: {e}")

        @self.bot.command(name="names")
        async def name_generator(
            ctx, element_type: str, genre: str, setting: str, *, culture: str = ""
        ):
            """Generate creative names (like Sudowrite's name generation)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🏷️ Generating names...")
                names = writing_assistant.name_generator(
                    element_type, genre, setting, culture
                )

                if names:
                    names_text = "\n".join([f"• {name}" for name in names])
                    await self._send_long_message(
                        ctx, names_text, f"🏷️ **{element_type.title()} Names:**"
                    )
                else:
                    await ctx.send("❌ No names generated")

            except Exception as e:
                logger.error(f"❌ Error generating names: {e}")
                await ctx.send(f"❌ Error generating names: {e}")

        @self.bot.command(name="plot-twist")
        async def plot_twist(ctx, current_plot: str, genre: str):
            """Generate unexpected plot twists"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                writing_assistant = self.framework.get_plugin("writing_assistant")
                if not writing_assistant:
                    await ctx.send("❌ Writing Assistant plugin not available")
                    return

                await ctx.send("🔄 Generating plot twists...")
                twists = writing_assistant.plot_twist_generator(current_plot, genre)

                if twists:
                    twists_text = "\n".join([f"• {twist}" for twist in twists])
                    await self._send_long_message(
                        ctx, twists_text, "🔄 **Plot Twists:**"
                    )
                else:
                    await ctx.send("❌ No plot twists generated")

            except Exception as e:
                logger.error(f"❌ Error generating plot twists: {e}")
                await ctx.send(f"❌ Error generating plot twists: {e}")

        # Personality Commands
        @self.bot.command(name="personality")
        async def personality_command(ctx, action: str = "show"):
            """Show or evolve Luna's personality"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                personality_engine = self.framework.get_plugin("personality_engine")
                if not personality_engine:
                    await ctx.send("❌ Personality Engine plugin not available")
                    return

                if action.lower() == "show":
                    # Show personality summary
                    summary = personality_engine.get_personality_summary()
                    await self._send_long_message(
                        ctx, summary, "🌟 **Luna's Personality:**"
                    )

                    # Show learning stats
                    stats = personality_engine.get_personality_stats()

                    embed = discord.Embed(
                        title="📊 Learning Progress",
                        color=0x9B59B6,
                        timestamp=datetime.now(),
                    )

                    if stats["conversation_patterns"]:
                        patterns = stats["conversation_patterns"]
                        embed.add_field(
                            name="💬 Conversation Patterns",
                            value=f"Avg Message Length: {patterns.get('avg_message_length', 0):.0f} chars\n"
                            f"Emoji Usage: {patterns.get('emoji_frequency', 0)*100:.1f}%\n"
                            f"Formality Level: {patterns.get('formality_level', 0)*100:.1f}%",
                            inline=True,
                        )

                    if stats["user_preferences"]:
                        top_preferences = list(stats["user_preferences"].items())[:5]
                        preferences_text = "\n".join(
                            [
                                f"• {topic}: {count} times"
                                for topic, count in top_preferences
                            ]
                        )
                        embed.add_field(
                            name="🎯 Your Preferences",
                            value=preferences_text,
                            inline=True,
                        )

                    await ctx.send(embed=embed)

                elif action.lower() == "evolve":
                    await ctx.send(
                        "🔄 Evolving Luna's personality based on our interactions..."
                    )
                    personality_engine.evolve_personality()
                    await ctx.send(
                        "✅ Luna's personality has evolved! She's learning and adapting to your style! ✨"
                    )

                else:
                    await ctx.send("❌ Unknown action. Use: `show` or `evolve`")

            except Exception as e:
                logger.error(f"❌ Error in personality command: {e}")
                await ctx.send(f"❌ Error: {str(e)}")

        @self.bot.command(name="personality-test")
        async def personality_test_command(ctx, test_type: str = "writing_style"):
            """Start a personality test to customize Luna's behavior"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                personality_test_engine = self.framework.get_plugin(
                    "personality_test_engine"
                )
                if not personality_test_engine:
                    await ctx.send("❌ Personality test engine not available.")
                    return

                # Start the test
                test_session = personality_test_engine.start_personality_test(test_type)

                if "error" in test_session:
                    await ctx.send(f"❌ {test_session['error']}")
                    return

                # Display the first question
                question = test_session["question"]
                options_text = "\n".join(
                    [
                        f"{i+1}. {opt['text']}"
                        for i, opt in enumerate(question["options"])
                    ]
                )

                test_message = f"""🧠 **{test_session['title']}**

{test_session['description']}

**Question {test_session['current_question'] + 1} of {test_session['total_questions']}:**
{question['question']}

**Options:**
{options_text}

**To answer:** `!test-answer {test_session['session_id']} {question['id']} <option_number>`

**Available tests:** `writing_style`, `communication_style`, `learning_preferences`
"""
                await self._send_long_message(
                    ctx, test_message, "📝 **PERSONALITY TEST**"
                )

            except Exception as e:
                await ctx.send(f"❌ Failed to start personality test: {str(e)}")

        @self.bot.command(name="test-answer")
        async def test_answer_command(
            ctx, session_id: str, question_id: str, answer_index: int
        ):
            """Submit an answer to a personality test question"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                personality_test_engine = self.framework.get_plugin(
                    "personality_test_engine"
                )
                if not personality_test_engine:
                    await ctx.send("❌ Personality test engine not available.")
                    return

                # Submit the answer
                result = personality_test_engine.submit_test_answer(
                    session_id, question_id, answer_index - 1
                )  # Convert to 0-based index

                if "error" in result:
                    await ctx.send(f"❌ {result['error']}")
                    return

                # Show the changes
                changes_text = "\n".join(
                    [
                        f"  {trait.title()}: {change:+.3f}"
                        for trait, change in result["weight_changes"].items()
                    ]
                )

                response = f"""✅ **Answer Recorded!**

**Changes Applied:**
{changes_text}

**Next:** Use `!personality-test <test_type>` to start another test or `!personality show` to see Luna's current personality.
"""
                await ctx.send(response)

            except Exception as e:
                await ctx.send(f"❌ Failed to submit answer: {str(e)}")

        @self.bot.command(name="learning-summary")
        async def learning_summary_command(ctx):
            """Show Luna's learning progress and personality evolution"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                enhanced_learning_engine = self.framework.get_plugin(
                    "enhanced_learning_engine"
                )
                if not enhanced_learning_engine:
                    await ctx.send("❌ Enhanced learning engine not available.")
                    return

                summary = enhanced_learning_engine.get_learning_summary()
                await self._send_long_message(
                    ctx, summary, "🧠 **LUNA'S LEARNING PROGRESS**"
                )

            except Exception as e:
                await ctx.send(f"❌ Failed to get learning summary: {str(e)}")

        @self.bot.command(name="modify-message")
        async def modify_message_command(ctx, modification_type: str, *, message: str):
            """Modify a message to make it easier for Luna to understand"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                enhanced_learning_engine = self.framework.get_plugin(
                    "enhanced_learning_engine"
                )
                if not enhanced_learning_engine:
                    await ctx.send("❌ Enhanced learning engine not available")
                    return

                modified_message = (
                    enhanced_learning_engine.modify_message_for_understanding(
                        message, modification_type
                    )
                )

                response = f"""🔧 **Message Modified**

**Original:** {message}
**Modified:** {modified_message}
**Type:** {modification_type}

**Available types:** `simplify`, `clarify`, `expand`
"""
                await ctx.send(response)

            except Exception as e:
                await ctx.send(f"❌ Failed to modify message: {str(e)}")

        @self.bot.command(name="reward-learning")
        async def reward_learning_command(ctx, activity: str, success_level: float):
            """Reward Luna for learning activities (for testing)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                enhanced_learning_engine = self.framework.get_plugin(
                    "enhanced_learning_engine"
                )
                if not enhanced_learning_engine:
                    await ctx.send("❌ Enhanced learning engine not available")
                    return

                enhanced_learning_engine._reward_learning(activity, success_level)
                await ctx.send(
                    f"🎉 **Learning Rewarded!**\n\n**Activity:** {activity}\n**Success Level:** {success_level:.2f}"
                )

            except Exception as e:
                await ctx.send(f"❌ Failed to reward learning: {str(e)}")

        @self.bot.command(name="punish-learning")
        async def punish_learning_command(
            ctx, missed_opportunity: str, severity: float
        ):
            """Punish Luna for missed learning opportunities (for testing)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                enhanced_learning_engine = self.framework.get_plugin(
                    "enhanced_learning_engine"
                )
                if not enhanced_learning_engine:
                    await ctx.send("❌ Enhanced learning engine not available")
                    return

                enhanced_learning_engine._punish_lack_of_learning(
                    missed_opportunity, severity
                )
                await ctx.send(
                    f"⚠️ **Learning Punished!**\n\n**Missed Opportunity:** {missed_opportunity}\n**Severity:** {severity:.2f}"
                )

            except Exception as e:
                await ctx.send(f"❌ Failed to punish learning: {str(e)}")

        @self.bot.command(name="test-emotion")
        async def test_emotion_command(ctx, *, message: str):
            """Test the dynamic emotion adaptation system"""
            try:
                # Import the dynamic emotion engine
                import sys
                import os

                sys.path.append(
                    os.path.join(
                        os.path.dirname(__file__), "..", "astra_emotional_fragments"
                    )
                )

                from dynamic_emotion_engine import DynamicEmotionEngine

                # Initialize the engine
                engine = DynamicEmotionEngine()

                # Handle the context switch
                context_switch = engine.handle_rapid_context_switch(message)
                response = engine.generate_contextual_response(message, context_switch)

                # Create response embed
                embed = discord.Embed(
                    title="🎭 Dynamic Emotion Test",
                    description=f"**User Message:** {message}",
                    color=0x9B59B6,
                )

                embed.add_field(name="AI Response", value=response, inline=False)

                embed.add_field(
                    name="Current Emotion",
                    value=engine.current_emotion or "None",
                    inline=True,
                )

                embed.add_field(
                    name="Detected Topics",
                    value=", ".join(context_switch["context"]["topics"]) or "None",
                    inline=True,
                )

                embed.add_field(
                    name="Action", value=context_switch["action"], inline=True
                )

                if context_switch["action"] == "transition":
                    transition = context_switch["transition"]
                    embed.add_field(
                        name="Transition",
                        value=f"{transition['from_emotion']} → {transition['to_emotion']}",
                        inline=False,
                    )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error testing emotion system: {str(e)}")

        @self.bot.command(name="blend-emotions")
        async def blend_emotions_command(
            ctx, primary: str, secondary: str = None, tertiary: str = None
        ):
            """Blend multiple emotions to create a complex emotional state"""
            try:
                # Import the emotional blender
                import sys
                import os

                sys.path.append(
                    os.path.join(
                        os.path.dirname(__file__), "..", "astra_emotional_fragments"
                    )
                )

                from emotional_blender import EmotionalBlender

                blender = EmotionalBlender()

                # Create the blend
                if secondary and tertiary:
                    emotions = [primary, secondary, tertiary]
                    weights = [0.5, 0.3, 0.2]  # Primary gets highest weight
                    blended = blender.create_complex_emotion(emotions, weights)
                elif secondary:
                    blended = blender.blend_emotions(primary, [secondary])
                else:
                    # Just show the primary emotion
                    emotion_data = blender.fragments.get(primary.lower())
                    if emotion_data:
                        blended = {
                            "name": emotion_data["name"],
                            "description": emotion_data["description"],
                            "keywords": emotion_data["keywords"],
                            "phrases": emotion_data["phrases"],
                        }
                    else:
                        await ctx.send(f"❌ Unknown emotion: {primary}")
                        return

                # Create response embed
                embed = discord.Embed(
                    title=f"🎭 {blended['name']}",
                    description=blended["description"],
                    color=0xE74C3C,
                )

                embed.add_field(
                    name="Keywords", value=", ".join(blended["keywords"]), inline=False
                )

                embed.add_field(
                    name="Example Phrases",
                    value="\n".join(
                        [f"• {phrase}" for phrase in blended["phrases"][:3]]
                    ),
                    inline=False,
                )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error blending emotions: {str(e)}")

        @self.bot.command(name="test-prompt-injection")
        async def test_prompt_injection_command(ctx, *, message: str):
            """Test the prompt injection system"""
            try:
                import sys
                import os

                sys.path.append(
                    os.path.join(
                        os.path.dirname(__file__), "..", "astra_emotional_fragments"
                    )
                )
                from prompt_injection_engine import PromptInjectionEngine

                engine = PromptInjectionEngine()
                injection_result = engine.inject_emotional_context(message)

                embed = discord.Embed(
                    title="🎭 Prompt Injection Test",
                    description=f"**User Message:** {message}",
                    color=0xE74C3C,
                )
                embed.add_field(
                    name="Current Emotion",
                    value=injection_result["current_emotion"],
                    inline=True,
                )
                embed.add_field(
                    name="Detected Topics",
                    value=", ".join(injection_result["detected_topics"]) or "None",
                    inline=True,
                )
                embed.add_field(
                    name="Intensity", value=injection_result["intensity"], inline=True
                )

                if injection_result["emotion_context"].get("transition"):
                    transition = injection_result["emotion_context"]
                    embed.add_field(
                        name="Emotional Transition",
                        value=f"{transition['from_emotion']} → {transition['to_emotion']}",
                        inline=False,
                    )

                # Show a sample of the injected prompt
                prompt_sample = (
                    injection_result["injected_prompt"][:500] + "..."
                    if len(injection_result["injected_prompt"]) > 500
                    else injection_result["injected_prompt"]
                )
                embed.add_field(
                    name="Injected Prompt Sample",
                    value=f"```{prompt_sample}```",
                    inline=False,
                )

                embed.add_field(
                    name="Prompt Length",
                    value=f"{len(injection_result['injected_prompt'])} characters",
                    inline=True,
                )

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error testing prompt injection: {str(e)}")

        @self.bot.command(name="generate-multimodal")
        async def generate_multimodal_command(ctx, *, args: str = ""):
            """Generate multimodal content (text, image, voice, video, audio)"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments
                import shlex

                parsed_args = shlex.split(args)

                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!generate-multimodal "A romantic sunset scene" text,image,voice romantic`'
                    )
                    return

                prompt = parsed_args[0]
                media_types = ["text", "image"]  # Default
                style = "default"

                if len(parsed_args) > 1:
                    media_types = [mt.strip() for mt in parsed_args[1].split(",")]
                if len(parsed_args) > 2:
                    style = parsed_args[2]

                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Generate content
                results = await multimodal.generate_multimodal_content(
                    text_prompt=prompt, media_types=media_types, style=style
                )

                # Create embed response
                embed = discord.Embed(
                    title="🎭 Multimodal Content Generated",
                    description=f"**Prompt:** {prompt}",
                    color=0x9B59B6,
                )

                for media_type, result in results.items():
                    if isinstance(result, dict):
                        if result.get("success"):
                            embed.add_field(
                                name=f"✅ {media_type.title()}",
                                value=f"Generated: {result.get('path', 'Success')}",
                                inline=True,
                            )
                        else:
                            embed.add_field(
                                name=f"❌ {media_type.title()}",
                                value=f"Error: {result.get('error', 'Unknown error')}",
                                inline=True,
                            )
                    else:
                        embed.add_field(
                            name=f"📄 {media_type.title()}",
                            value=f"{str(result)[:100]}...",
                            inline=False,
                        )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error generating multimodal content: {str(e)}")

        @self.bot.command(name="create-character-media")
        async def create_character_media_command(
            ctx, character_name: str, *, description: str = ""
        ):
            """Create multimedia content for a character"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Create character data
                character_data = {
                    "description": description or f"A character named {character_name}",
                    "voice_description": f"I am {character_name}, a character with unique personality",
                    "style": "default",
                    "voice_style": "default",
                }

                # Generate character multimedia
                results = await multimodal.create_character_multimedia(
                    character_name=character_name,
                    character_data=character_data,
                    media_types=["image", "voice", "text"],
                )

                # Create embed response
                embed = discord.Embed(
                    title=f"🎭 Character Media: {character_name}",
                    description=f"**Description:** {character_data['description']}",
                    color=0xE74C3C,
                )

                for media_type, result in results.items():
                    if isinstance(result, dict):
                        if result.get("success"):
                            embed.add_field(
                                name=f"✅ {media_type.replace('_', ' ').title()}",
                                value=f"Generated: {result.get('path', 'Success')}",
                                inline=True,
                            )
                        else:
                            embed.add_field(
                                name=f"❌ {media_type.replace('_', ' ').title()}",
                                value=f"Error: {result.get('error', 'Unknown error')}",
                                inline=True,
                            )
                    else:
                        embed.add_field(
                            name=f"📄 {media_type.replace('_', ' ').title()}",
                            value=f"{str(result)[:100]}...",
                            inline=False,
                        )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error creating character media: {str(e)}")

        @self.bot.command(name="create-story-media")
        async def create_story_media_command(
            ctx, story_title: str, genre: str, *, description: str = ""
        ):
            """Create multimedia content for a story"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Create story data
                story_data = {
                    "genre": genre,
                    "description": description or f"A {genre} story",
                    "style": "default",
                }

                # Generate story multimedia
                results = await multimodal.create_story_multimedia(
                    story_title=story_title,
                    story_data=story_data,
                    media_types=["image", "video", "text"],
                )

                # Create embed response
                embed = discord.Embed(
                    title=f"📚 Story Media: {story_title}",
                    description=f"**Genre:** {genre}\n**Description:** {story_data['description']}",
                    color=0x3498DB,
                )

                for media_type, result in results.items():
                    if isinstance(result, dict):
                        if result.get("success"):
                            embed.add_field(
                                name=f"✅ {media_type.replace('_', ' ').title()}",
                                value=f"Generated: {result.get('path', 'Success')}",
                                inline=True,
                            )
                        else:
                            embed.add_field(
                                name=f"❌ {media_type.replace('_', ' ').title()}",
                                value=f"Error: {result.get('error', 'Unknown error')}",
                                inline=True,
                            )
                    else:
                        embed.add_field(
                            name=f"📄 {media_type.replace('_', ' ').title()}",
                            value=f"{str(result)[:100]}...",
                            inline=False,
                        )

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Error creating story media: {str(e)}")

        @self.bot.command(name="generate-image")
        async def generate_image_command(ctx, *, args: str = ""):
            """Generate image using Stable Diffusion"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments
                import shlex

                parsed_args = shlex.split(args)

                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!generate-image "A romantic sunset scene" romantic`'
                    )
                    return

                prompt = parsed_args[0]
                style = parsed_args[1] if len(parsed_args) > 1 else "default"

                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Generate image
                result = await multimodal._generate_image_with_stable_diffusion(
                    prompt, style
                )

                if result.get("success"):
                    embed = discord.Embed(
                        title="🎨 Image Generated",
                        description=f"**Prompt:** {prompt}\n**Style:** {style}",
                        color=0x2ECC71,
                    )
                    embed.add_field(
                        name="✅ Success",
                        value=f"Generated: {result.get('path', 'Success')}",
                        inline=True,
                    )
                    embed.add_field(
                        name="📏 Size",
                        value=f"{result.get('size', 'Unknown')}",
                        inline=True,
                    )

                    # Try to attach the image file
                    try:
                        file_path = result.get("path")
                        if file_path and os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file = discord.File(
                                    f,
                                    filename=f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                )
                                await ctx.send(embed=embed, file=file)
                        else:
                            await ctx.send(embed=embed)
                    except Exception as e:
                        await ctx.send(embed=embed)
                        await ctx.send(f"⚠️ Could not attach image file: {str(e)}")
                else:
                    await ctx.send(
                        f"❌ Error generating image: {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                await ctx.send(f"❌ Error generating image: {str(e)}")

        @self.bot.command(name="generate-voice")
        async def generate_voice_command(ctx, *, args: str = ""):
            """Generate voice from text"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments
                import shlex

                parsed_args = shlex.split(args)

                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide text. Example: `!generate-voice "Hello, I am Luna" romantic`'
                    )
                    return

                text = parsed_args[0]
                style = parsed_args[1] if len(parsed_args) > 1 else "default"

                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Generate voice
                result = await multimodal._generate_voice_with_tts(text, style)

                if result.get("success"):
                    embed = discord.Embed(
                        title="🎤 Voice Generated",
                        description=f"**Text:** {text}\n**Style:** {style}",
                        color=0xE67E22,
                    )
                    embed.add_field(
                        name="✅ Success",
                        value=f"Generated: {result.get('path', 'Success')}",
                        inline=True,
                    )
                    embed.add_field(
                        name="⏱️ Duration",
                        value=f"{result.get('duration', 'Unknown')}",
                        inline=True,
                    )

                    # Try to attach the audio file
                    try:
                        file_path = result.get("path")
                        if file_path and os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file = discord.File(
                                    f,
                                    filename=f"generated_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                                )
                                await ctx.send(embed=embed, file=file)
                        else:
                            await ctx.send(embed=embed)
                    except Exception as e:
                        await ctx.send(embed=embed)
                        await ctx.send(f"⚠️ Could not attach audio file: {str(e)}")
                else:
                    await ctx.send(
                        f"❌ Error generating voice: {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                await ctx.send(f"❌ Error generating voice: {str(e)}")

        @self.bot.command(name="generate-video")
        async def generate_video_command(ctx, *, args: str = ""):
            """Generate video from prompt"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments
                import shlex

                parsed_args = shlex.split(args)

                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!generate-video "A romantic scene" 15`'
                    )
                    return

                prompt = parsed_args[0]
                duration = int(parsed_args[1]) if len(parsed_args) > 1 else 15

                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Generate video
                result = await multimodal._generate_video_with_model(prompt, "default")

                if result.get("success"):
                    embed = discord.Embed(
                        title="🎬 Video Generated",
                        description=f"**Prompt:** {prompt}\n**Duration:** {duration}s",
                        color=0x9B59B6,
                    )
                    embed.add_field(
                        name="✅ Success",
                        value=f"Generated: {result.get('path', 'Success')}",
                        inline=True,
                    )
                    embed.add_field(
                        name="⏱️ Duration",
                        value=f"{result.get('duration', 'Unknown')}",
                        inline=True,
                    )

                    # Try to attach the video file
                    try:
                        file_path = result.get("path")
                        if file_path and os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file = discord.File(
                                    f,
                                    filename=f"generated_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                                )
                                await ctx.send(embed=embed, file=file)
                        else:
                            await ctx.send(embed=embed)
                    except Exception as e:
                        await ctx.send(embed=embed)
                        await ctx.send(f"⚠️ Could not attach video file: {str(e)}")
                else:
                    await ctx.send(
                        f"❌ Error generating video: {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                await ctx.send(f"❌ Error generating video: {str(e)}")

        @self.bot.command(name="generate-sound")
        async def generate_sound_command(ctx, *, args: str = ""):
            """Generate sound effects"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return

            try:
                # Parse arguments
                import shlex

                parsed_args = shlex.split(args)

                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!generate-sound "Romantic atmosphere" romantic`'
                    )
                    return

                prompt = parsed_args[0]
                style = parsed_args[1] if len(parsed_args) > 1 else "default"

                # Get multimodal orchestrator
                multimodal = self.framework.get_plugin("multimodal_orchestrator")
                if not multimodal:
                    await ctx.send("❌ Multimodal orchestrator not available")
                    return

                # Generate sound
                result = await multimodal._generate_sound_effects(prompt, style)

                if result.get("success"):
                    embed = discord.Embed(
                        title="🔊 Sound Generated",
                        description=f"**Prompt:** {prompt}\n**Style:** {style}",
                        color=0xF39C12,
                    )
                    embed.add_field(
                        name="✅ Success",
                        value=f"Generated: {result.get('path', 'Success')}",
                        inline=True,
                    )
                    embed.add_field(
                        name="🎵 Type",
                        value=f"{result.get('type', 'Sound Effect')}",
                        inline=True,
                    )

                    # Try to attach the audio file
                    try:
                        file_path = result.get("path")
                        if file_path and os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file = discord.File(
                                    f,
                                    filename=f"generated_sound_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                                )
                                await ctx.send(embed=embed, file=file)
                        else:
                            await ctx.send(embed=embed)
                    except Exception as e:
                        await ctx.send(embed=embed)
                        await ctx.send(f"⚠️ Could not attach audio file: {str(e)}")
                else:
                    await ctx.send(
                        f"❌ Error generating sound: {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                await ctx.send(f"❌ Error generating sound: {str(e)}")

    async def _handle_natural_language(self, ctx, message: str) -> str:
        """Handle natural language requests"""
        try:
            # Use the tool manager to handle natural language
            result = self.framework.call_with_tools(message)

            # Clean up the response
            if isinstance(result, dict):
                if "content" in result:
                    content = result["content"]
                    # Remove thinking process if present
                    if "<think>" in content and "</think>" in content:
                        start = content.find("</think>") + 8
                        content = content[start:].strip()
                    return content
                else:
                    return str(result)
            else:
                return str(result)
        except Exception as e:
            return f"Sorry, I couldn't process that request: {str(e)}"

    def _is_authorized(self, ctx) -> bool:
        """Check if user is authorized to use the bot"""
        user_id = str(ctx.author.id)
        channel_id = str(ctx.channel.id)

        return (
            user_id in self.config["allowed_users"]
            and channel_id in self.config["allowed_channels"]
        )

    def _split_message(self, message: str, max_length: int = 1900) -> List[str]:
        """Split long messages for Discord with improved logic"""
        if len(message) <= max_length:
            return [message]

        parts = []
        current_part = ""

        # Split by lines first, then by words if needed
        lines = message.split("\n")

        for line in lines:
            # If adding this line would exceed the limit
            if len(current_part) + len(line) + 1 > max_length:
                if current_part:
                    parts.append(current_part.strip())
                    current_part = line
                else:
                    # Single line is too long, split by words
                    words = line.split()
                    for word in words:
                        if len(current_part) + len(word) + 1 > max_length:
                            if current_part:
                                parts.append(current_part.strip())
                                current_part = word
                            else:
                                # Single word is too long, truncate
                                parts.append(word[: max_length - 3] + "...")
                                current_part = ""
                        else:
                            current_part += " " + word if current_part else word
            else:
                current_part += "\n" + line if current_part else line

        if current_part:
            parts.append(current_part.strip())

        # If the entire message is still too long, force split it
        if len(parts) == 1 and len(parts[0]) > max_length:
            # Force split the single part
            forced_parts = []
            remaining = parts[0]
            while len(remaining) > max_length:
                forced_parts.append(remaining[:max_length])
                remaining = remaining[max_length:]
            if remaining:
                forced_parts.append(remaining)
            return forced_parts
        elif len(parts) == 1 and len(parts[0]) <= max_length:
            # Check if the original message was longer than max_length
            if len(message) > max_length:
                # Force split the original message
                forced_parts = []
                remaining = message
                while len(remaining) > max_length:
                    forced_parts.append(remaining[:max_length])
                    remaining = remaining[max_length:]
                if remaining:
                    forced_parts.append(remaining)
                return forced_parts

        return parts

    async def _send_long_message(self, ctx, message: str, prefix: str = "") -> None:
        """Send a message that may be longer than Discord's limit"""
        # Handle both Context and TextChannel objects
        if hasattr(ctx, "channel"):
            # It's a Context object, use ctx.channel.send
            send_func = ctx.channel.send
        else:
            # It's a TextChannel object, use ctx.send
            send_func = ctx.send

        if len(message) <= 2000:
            if prefix:
                await send_func(f"{prefix}\n{message}")
            else:
                await send_func(message)
        else:
            parts = self._split_message(message, 1900)
            for i, part in enumerate(parts):
                if i == 0:
                    if prefix:
                        await send_func(f"{prefix}\n{part}")
                    else:
                        await send_func(part)
                else:
                    await send_func(f"(continued {i+1}/{len(parts)})\n{part}")

    async def start(self):
        """Start the Discord bot"""
        try:
            await self.bot.start(self.config["discord_token"])
        except Exception as e:
            logger.error(f"❌ Failed to start Discord bot: {e}")
            raise


def main():
    """Main entry point for the authoring bot"""
    bot = AuthoringBot()

    # Load data
    bot.framework.load_data()

    # Start the bot
    asyncio.run(bot.start())


if __name__ == "__main__":
    main()
