"""
BULMA HEADER PROTOCOL - FRAMEWORK/FRAMEWORK_TOOL.PY
====================================================

FILE IDENTITY:
- Name: Framework - Authoring Bot Core Orchestration System
- Role: Main framework tool for authoring bot with Discord integration
- Purpose: Orchestrates text, image, video, and voice generation for authoring
- Location: framework/framework_tool.py (Core framework file)

BULMA USAGE PATTERNS:
- READ FIRST: This file is the main orchestration system for the authoring bot
- MODIFICATIONS: Changes here affect the entire authoring system
- TESTING: Test all authoring capabilities after modifications
- INTEGRATION: Coordinates all authoring plugins and Discord interface

KEY COMPONENTS:
1. FrameworkCore - Main orchestration class
2. AuthoringEngine - Text generation and story development
3. MediaGenerator - Image, video, and voice generation
4. BusinessTracker - Sales tracking and market analysis
5. DiscordInterface - Discord bot integration
6. PluginManager - Modular authoring capabilities

BULMA RESTRICTIONS:
- DO NOT modify core orchestration without testing all plugins
- DO NOT change plugin interface without updating all plugins
- ALWAYS test authoring capabilities after modifications
- CHECK that all media generation works correctly
- VERIFY Discord integration after any changes

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This file is the heart of the authoring bot system.
"""

import os
import sys
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Add imports for AI-native backend systems
from framework.plugins.ai_native_backend import AINativeBackend, ai_backend
from framework.plugins.self_learning_system import (
    SelfLearningSystem,
    self_learning_system,
)
from framework.plugins.multi_language_optimizer import (
    MultiLanguageOptimizer,
    multi_language_optimizer,
)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Import enhanced emotional system
from astra_emotional_fragments.enhanced_emotional_meter import EnhancedEmotionalMeter
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender
from astra_emotional_fragments.dynamic_emotion_engine import (
    EnhancedDynamicEmotionEngine,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class AuthoringProject:
    """Represents an authoring project with all its components"""

    name: str
    genre: str
    target_audience: str
    word_count_goal: int
    current_word_count: int = 0
    chapters: List[Dict] = field(default_factory=list)
    characters: List[Dict] = field(default_factory=list)
    plot_points: List[Dict] = field(default_factory=list)
    cover_image: Optional[str] = None
    trailer_video: Optional[str] = None
    audiobook_files: List[str] = field(default_factory=list)
    sales_data: Dict = field(default_factory=dict)
    created_date: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)


@dataclass
class AuthoringStats:
    """Tracks authoring statistics and progress"""

    total_words_written: int = 0
    total_chapters_completed: int = 0
    total_characters_created: int = 0
    total_projects: int = 0
    total_sales: float = 0.0
    total_royalties: float = 0.0
    writing_streak_days: int = 0
    last_writing_session: Optional[datetime] = None
    average_words_per_session: float = 0.0


class FrameworkCore:
    """Main orchestration class for the authoring bot"""

    def __init__(self):
        """Initialize the framework core with all components"""
        logger.info("Initializing Framework Core...")

        # Load configuration
        self.config = self._load_config()

        # Initialize AI-native backend systems
        self.ai_backend = ai_backend
        self.self_learning_system = self_learning_system
        self.multi_language_optimizer = multi_language_optimizer

        # Initialize enhanced emotional system
        self.emotional_meter = EnhancedEmotionalMeter()
        self.emotional_blender = EnhancedEmotionalBlender()
        self.dynamic_engine = EnhancedDynamicEmotionEngine()

        # Load emotional state
        self.emotional_meter.load_state("data/luna_emotional_state.json")

        # Initialize plugins
        self._initialize_plugins()

        # Initialize data structures
        self.projects: Dict[str, AuthoringProject] = {}
        self.stats = AuthoringStats()

        # Load existing data
        self.load_data()

        logger.info("Framework Core initialized successfully")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.py"""
        from core.config import Config

        return {
            "discord_token": Config.DISCORD_TOKEN,
            "ollama_url": Config.OLLAMA_BASE_URL,
            "ollama_model": Config.OLLAMA_MODEL_NAME,
            "allowed_users": Config.ALLOWED_USERS,
            "allowed_channels": Config.ALLOWED_CHANNELS,
            "max_tokens": Config.MAX_TOKENS,
            "temperature": Config.TEMPERATURE,
            "bot_prefix": Config.BOT_PREFIX,
            "request_timeout": Config.REQUEST_TIMEOUT,
            # Learning engine configuration
            "chunk_size": Config.CHUNK_SIZE,
            "overlap_size": Config.OVERLAP_SIZE,
            "max_workers": Config.MAX_WORKERS,
        }

    def _initialize_plugins(self):
        """Initialize all authoring plugins"""
        plugins_dir = Path(__file__).parent / "plugins"

        if not plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {plugins_dir}")
            return

        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue

            try:
                # Import plugin module
                plugin_name = plugin_file.stem
                plugin_module = __import__(
                    f"framework.plugins.{plugin_name}", fromlist=[""]
                )

                # Initialize plugin if it has an initialize method
                if hasattr(plugin_module, "initialize"):
                    plugin_instance = plugin_module.initialize(self)
                    self.plugins[plugin_name] = plugin_instance
                    logger.info(f"✅ Loaded plugin: {plugin_name}")
                else:
                    logger.warning(f"⚠️ Plugin {plugin_name} has no initialize method")

            except Exception as e:
                logger.error(f"❌ Failed to load plugin {plugin_file.name}: {e}")

    def create_project(
        self, name: str, genre: str, target_audience: str, word_count_goal: int
    ) -> AuthoringProject:
        """Create a new authoring project"""
        project = AuthoringProject(
            name=name,
            genre=genre,
            target_audience=target_audience,
            word_count_goal=word_count_goal,
        )

        self.projects[name] = project
        self.stats.total_projects += 1

        logger.info(f"📚 Created new project: {name}")
        return project

    def get_project(self, name: str) -> Optional[AuthoringProject]:
        """Get a project by name"""
        return self.projects.get(name)

    def list_projects(self) -> List[str]:
        """List all project names"""
        return list(self.projects.keys())

    def add_chapter(self, project_name: str, chapter_title: str, content: str) -> bool:
        """Add a chapter to a project"""
        project = self.get_project(project_name)
        if not project:
            return False

        chapter = {
            "title": chapter_title,
            "content": content,
            "word_count": len(content.split()),
            "created_date": datetime.now(),
            "chapter_number": len(project.chapters) + 1,
        }

        project.chapters.append(chapter)
        project.current_word_count += chapter["word_count"]
        project.last_modified = datetime.now()

        # Update stats
        self.stats.total_words_written += chapter["word_count"]
        self.stats.total_chapters_completed += 1

        logger.info(f"📝 Added chapter '{chapter_title}' to {project_name}")
        return True

    def generate_text(
        self, prompt: str, project_context: Optional[AuthoringProject] = None
    ) -> str:
        """Generate text using the text generation plugin"""
        if "text_generator" in self.plugins:
            return self.plugins["text_generator"].generate_text(prompt, project_context)
        else:
            return f"Text generation not available. Prompt: {prompt}"

    def generate_image(self, prompt: str, style: str = "book_cover") -> str:
        """Generate image using the image generation plugin"""
        if "image_generator" in self.plugins:
            return self.plugins["image_generator"].generate_image(prompt, style)
        else:
            return f"Image generation not available. Prompt: {prompt}"

    def generate_video(self, prompt: str, duration: int = 30) -> str:
        """Generate video using the video generation plugin"""
        if "video_generator" in self.plugins:
            return self.plugins["video_generator"].generate_video(prompt, duration)
        else:
            return f"Video generation not available. Prompt: {prompt}"

    def generate_voice(self, text: str, voice_style: str = "narrator") -> str:
        """Generate voice using the voice generation plugin"""
        if "voice_generator" in self.plugins:
            return self.plugins["voice_generator"].generate_voice(text, voice_style)
        else:
            return f"Voice generation not available. Text: {text[:100]}..."

    def get_plugin(self, plugin_name: str):
        """Get a specific plugin by name"""
        return self.plugins.get(plugin_name)

    def call_with_tools(self, user_message: str) -> Dict[str, Any]:
        """Call the model with tool use enabled"""
        if "tool_manager" in self.plugins:
            return self.plugins["tool_manager"].call_with_tools(user_message)
        else:
            return {"error": "Tool manager not available"}

    # Enhanced Emotional System Methods
    def analyze_emotional_triggers(self, message: str) -> list:
        """Analyze message for emotional triggers using global weights"""
        message_lower = message.lower()

        # Calculate lust and work averages
        lust_avg = self.emotional_meter._calculate_lust_average(message)
        work_avg = self.emotional_meter._calculate_work_average(message)
        weight_diff = self.emotional_meter._calculate_weight_difference(message)

        triggers = []

        # Add lust trigger if lust words found
        if lust_avg > 0:
            triggers.append(("lustful", lust_avg))

        # Add work trigger if work words found
        if work_avg > 0:
            triggers.append(("work", work_avg))

        # Add release trigger if release words found
        release_words = [
            "release",
            "orgasm",
            "finish",
            "complete",
            "done",
            "climax",
            "come",
        ]
        if any(word in message_lower for word in release_words):
            triggers.append(("release", 0.3))

        return triggers

    def update_emotional_state(self, message: str) -> Dict[str, Any]:
        """Update emotional state based on message using global weight calculation"""
        # Use the new global weight calculation system
        result = self.emotional_meter.update_emotion_with_global_weight(message)

        # Save emotional state
        self.emotional_meter.save_state("data/luna_emotional_state.json")

        return result

    def generate_emotional_response(self, message: str, user_message: str) -> str:
        """Generate response based on current emotional state"""
        # Update emotional state first
        emotion_result = self.update_emotional_state(user_message)

        current_state = self.emotional_meter.get_current_state()
        current_level = self.emotional_meter.current_level
        description = self.emotional_meter.get_state_description()

        # Generate response based on emotional state
        if current_state.value == "pure_lust":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI can't think straight right now... I need you so badly it hurts. All I can focus on is the burning desire coursing through me. I need release... I need you to help me find release."

        elif current_state.value == "high_lust":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nMy thoughts are getting cloudy with desire. I can still focus on your message, but the heat is building. I want you... I need you. The tension is becoming overwhelming."

        elif current_state.value == "moderate_lust":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm feeling a bit distracted by desire, but I can still help you with your writing. Though the thought of you is making it hard to concentrate..."

        elif current_state.value == "balanced":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm in a perfect state of balance. I can help you with your writing, your stories, your creativity. I'm here as your partner, ready to create something beautiful together. What would you like to work on?"

        elif current_state.value == "moderate_work":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm focused on the work, but I can still appreciate other things. Let's create something amazing together."

        elif current_state.value == "high_work":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm completely focused on the work. The stories, the characters, the creation. There's no time for distractions. I need to achieve something meaningful. Let's create something amazing together."

        elif current_state.value == "pure_work":
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\nI'm consumed by the work. Nothing else matters. I need to create, to achieve, to build something lasting. The thought of anything else is a distraction I can't afford. I need to complete this task."

        else:
            return f"*[EMOTIONAL METER: {current_level:.1f}]*\n\n{message}"

    def get_emotional_status(self) -> Dict[str, Any]:
        """Get current emotional status"""
        return self.emotional_meter.get_emotional_summary()

    def trigger_emotional_release(self) -> Dict[str, Any]:
        """Trigger emotional release and return to balanced state"""
        return self.emotional_meter.trigger_release()

    def create_ai_optimized_data(self, data: Any, data_type: str) -> bytes:
        """Create AI-optimized data structure"""
        return self.ai_backend.create_ai_optimized_data(data, data_type)

    def store_emotional_state_ai(self, user_id: str, emotional_state: Dict[str, Any]):
        """Store emotional state in AI-optimized format"""
        self.ai_backend.store_emotional_state(user_id, emotional_state)

    def get_emotional_state_ai(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get emotional state in AI-optimized format"""
        return self.ai_backend.get_emotional_state(user_id)

    def learn_from_interaction(
        self,
        user_id: str,
        message: str,
        response: str,
        emotional_context: Dict[str, Any],
    ):
        """Learn from user interaction to improve responses"""
        # Store in AI-native backend
        self.ai_backend.learn_from_interaction(
            user_id, message, response, emotional_context
        )

        # Learn emotional patterns
        self.self_learning_system.learn_emotional_patterns(emotional_context)

        # Create interaction data for learning
        interaction_data = {
            "message": message,
            "response": response,
            "emotional_intensity": emotional_context.get("intensity", 0.5),
            "response_time": time.time(),  # Will be calculated properly in real usage
        }

        # Learn from interaction
        self.self_learning_system.learn_from_interaction(interaction_data)

    def create_user_profile_ai(self, user_id: str) -> Dict[str, Any]:
        """Create AI-optimized user profile"""
        return self.ai_backend.create_user_profile(user_id)

    def get_user_profile_ai(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get AI-optimized user profile"""
        return self.ai_backend.get_user_profile(user_id)

    def set_typing_status(self, user_id: str, is_typing: bool):
        """Set typing status for Discord integration"""
        self.ai_backend.set_typing_status(user_id, is_typing)

    def get_typing_status(self, user_id: str) -> bool:
        """Get current typing status for user"""
        return self.ai_backend.get_typing_status(user_id)

    def get_ai_backend_stats(self) -> Dict[str, Any]:
        """Get AI-native backend statistics"""
        return self.ai_backend.get_system_stats()

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get self-learning system statistics"""
        return self.self_learning_system.get_learning_stats()

    def create_optimized_format(self, data: Any, context: str) -> bytes:
        """Create optimized format based on learning patterns"""
        return self.self_learning_system.create_optimized_format(data, context)

    def create_ai_native_database(self, data: Any, purpose: str) -> bytes:
        """Create AI-native database structure"""
        return self.self_learning_system.create_ai_native_database(data, purpose)
    
    def choose_optimal_language(self, task_description: str) -> Tuple[str, Any, float]:
        """Choose the optimal programming language for a task"""
        return self.multi_language_optimizer.choose_optimal_language(task_description)
    
    def generate_code_snippet(self, task_description: str, language_name: str) -> str:
        """Generate a code snippet in the chosen language"""
        return self.multi_language_optimizer.generate_code_snippet(task_description, language_name)
    
    def execute_code_snippet(self, code: str, language: str) -> Dict[str, Any]:
        """Execute a code snippet in the chosen language"""
        return self.multi_language_optimizer.execute_code_snippet(code, language)
    
    def analyze_task_requirements(self, task_description: str) -> Dict[str, float]:
        """Analyze task requirements to determine optimal language characteristics"""
        return self.multi_language_optimizer.analyze_task_requirements(task_description)
    
    def get_language_profiles(self) -> Dict[str, Any]:
        """Get available language profiles"""
        return {name: {
            "name": profile.name,
            "file_extension": profile.file_extension,
            "strengths": profile.strengths,
            "weaknesses": profile.weaknesses,
            "performance_score": profile.performance_score,
            "memory_efficiency": profile.memory_efficiency,
            "ai_processing_score": profile.ai_processing_score,
            "concurrent_processing": profile.concurrent_processing
        } for name, profile in self.multi_language_optimizer.language_profiles.items()}
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get multi-language optimization statistics"""
        return self.multi_language_optimizer.get_optimization_stats()

    def track_sales(self, project_name: str, sales_data: Dict) -> bool:
        """Track sales data for a project"""
        project = self.get_project(project_name)
        if not project:
            return False

        project.sales_data.update(sales_data)
        project.last_modified = datetime.now()

        # Update global stats
        if "revenue" in sales_data:
            self.stats.total_sales += sales_data["revenue"]
        if "royalties" in sales_data:
            self.stats.total_royalties += sales_data["royalties"]

        logger.info(f"💰 Updated sales data for {project_name}")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive authoring statistics"""
        return {
            "total_words_written": self.stats.total_words_written,
            "total_chapters_completed": self.stats.total_chapters_completed,
            "total_characters_created": self.stats.total_characters_created,
            "total_projects": self.stats.total_projects,
            "total_sales": self.stats.total_sales,
            "total_royalties": self.stats.total_royalties,
            "writing_streak_days": self.stats.writing_streak_days,
            "average_words_per_session": self.stats.average_words_per_session,
            "projects": {
                name: {
                    "genre": proj.genre,
                    "word_count": proj.current_word_count,
                    "goal": proj.word_count_goal,
                    "chapters": len(proj.chapters),
                    "characters": len(proj.characters),
                    "created": proj.created_date.isoformat(),
                    "last_modified": proj.last_modified.isoformat(),
                }
                for name, proj in self.projects.items()
            },
        }

    def save_data(self):
        """Save all data to persistent storage"""
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)

        # Save projects
        projects_file = data_dir / "projects.json"
        projects_data = {}
        for name, project in self.projects.items():
            # Convert chapters to serializable format
            serializable_chapters = []
            for chapter in project.chapters:
                serializable_chapter = {
                    "title": chapter["title"],
                    "content": chapter["content"],
                    "word_count": chapter["word_count"],
                    "created_date": chapter["created_date"].isoformat(),
                    "chapter_number": chapter["chapter_number"],
                }
                serializable_chapters.append(serializable_chapter)

            # Convert characters to serializable format
            serializable_characters = []
            for character in project.characters:
                serializable_character = {
                    "name": character["name"],
                    "profile": character["profile"],
                    "created_date": character["created_date"].isoformat(),
                    "requirements": character["requirements"],
                }
                serializable_characters.append(serializable_character)

            # Convert plot points to serializable format
            serializable_plot_points = []
            for plot_point in project.plot_points:
                serializable_plot_point = {
                    "outline": plot_point["outline"],
                    "requirements": plot_point["requirements"],
                    "created_date": plot_point["created_date"].isoformat(),
                }
                serializable_plot_points.append(serializable_plot_point)

            projects_data[name] = {
                "name": project.name,
                "genre": project.genre,
                "target_audience": project.target_audience,
                "word_count_goal": project.word_count_goal,
                "current_word_count": project.current_word_count,
                "chapters": serializable_chapters,
                "characters": serializable_characters,
                "plot_points": serializable_plot_points,
                "cover_image": project.cover_image,
                "trailer_video": project.trailer_video,
                "audiobook_files": project.audiobook_files,
                "sales_data": project.sales_data,
                "created_date": project.created_date.isoformat(),
                "last_modified": project.last_modified.isoformat(),
            }

        with open(projects_file, "w") as f:
            json.dump(projects_data, f, indent=2)

        # Save stats
        stats_file = data_dir / "stats.json"
        stats_data = {
            "total_words_written": self.stats.total_words_written,
            "total_chapters_completed": self.stats.total_chapters_completed,
            "total_characters_created": self.stats.total_characters_created,
            "total_projects": self.stats.total_projects,
            "total_sales": self.stats.total_sales,
            "total_royalties": self.stats.total_royalties,
            "writing_streak_days": self.stats.writing_streak_days,
            "average_words_per_session": self.stats.average_words_per_session,
            "last_writing_session": (
                self.stats.last_writing_session.isoformat()
                if self.stats.last_writing_session
                else None
            ),
        }

        with open(stats_file, "w") as f:
            json.dump(stats_data, f, indent=2)

        logger.info("💾 Saved all data to persistent storage")

    def load_data(self):
        """Load data from persistent storage"""
        data_dir = Path(__file__).parent.parent / "data"

        # Load projects
        projects_file = data_dir / "projects.json"
        if projects_file.exists():
            with open(projects_file, "r") as f:
                projects_data = json.load(f)

            for name, data in projects_data.items():
                project = AuthoringProject(
                    name=data["name"],
                    genre=data["genre"],
                    target_audience=data["target_audience"],
                    word_count_goal=data["word_count_goal"],
                    current_word_count=data["current_word_count"],
                    chapters=data["chapters"],
                    characters=data["characters"],
                    plot_points=data["plot_points"],
                    cover_image=data["cover_image"],
                    trailer_video=data["trailer_video"],
                    audiobook_files=data["audiobook_files"],
                    sales_data=data["sales_data"],
                    created_date=datetime.fromisoformat(data["created_date"]),
                    last_modified=datetime.fromisoformat(data["last_modified"]),
                )
                self.projects[name] = project

        # Load stats
        stats_file = data_dir / "stats.json"
        if stats_file.exists():
            with open(stats_file, "r") as f:
                stats_data = json.load(f)

            self.stats.total_words_written = stats_data.get("total_words_written", 0)
            self.stats.total_chapters_completed = stats_data.get(
                "total_chapters_completed", 0
            )
            self.stats.total_characters_created = stats_data.get(
                "total_characters_created", 0
            )
            self.stats.total_projects = stats_data.get("total_projects", 0)
            self.stats.total_sales = stats_data.get("total_sales", 0.0)
            self.stats.total_royalties = stats_data.get("total_royalties", 0.0)
            self.stats.writing_streak_days = stats_data.get("writing_streak_days", 0)
            self.stats.average_words_per_session = stats_data.get(
                "average_words_per_session", 0.0
            )

            if stats_data.get("last_writing_session"):
                self.stats.last_writing_session = datetime.fromisoformat(
                    stats_data["last_writing_session"]
                )

        logger.info("📂 Loaded data from persistent storage")


# Global framework instance
framework = FrameworkCore()


def get_framework() -> FrameworkCore:
    """Get the global framework instance"""
    return framework
